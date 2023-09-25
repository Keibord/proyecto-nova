from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin,  login_required, logout_user, current_user
from flask_login import login_user as flask_login_user



app = Flask(__name__)
bcrypt = Bcrypt(app)

# Configuración de la conexión a la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'nova'

mysql = MySQL(app)


# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_page'


class User(UserMixin):  # crea el usuario y le da sus atributos para acceder luego
    def __init__(self, username=None, user_type=None): # ataja type error
        self.id = username
        self.user_type = user_type

@login_manager.user_loader # Carga el usuario en sesion
def user_loader(username):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM usuario WHERE User = %s", [username])
    user_db = cursor.fetchone()

    if user_db:
        user = User(user_db[0], user_db[2])  # Asume que TipoUser es la tercera columna en tu tabla
        return user

@app.route('/register', methods=['GET', 'POST']) # registra un nuevo usuario
def register_user():
    if request.method == 'POST':
        username = request.form['username']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        tipo_user = request.form['user_type']
        admin_code = request.form.get('admin_code') # Obtiene el código de administrador

        if tipo_user == '1' and admin_code != '123': # Si el tipo de usuario es Administrador y el código de administrador no es correcto
            flash('Error, código de administrador incorrecto')
            return redirect(url_for('register_user')) # Redirige al usuario a la página de registro

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO usuario (User, Password, TipoUser) VALUES (%s, %s, %s)", (username, password, tipo_user))
        mysql.connection.commit()
        cursor.close()

        flash('Usuario registrado correctamente')
        return redirect(url_for('login_page'))

    return render_template('registro.html')


@app.route('/login_page')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST']) # inicia la sesion del usuario
def login_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM usuario WHERE User = %s", [username])
        user_db = cursor.fetchone()

        if user_db and bcrypt.check_password_hash(user_db[1], password):
            user = User()
            user.id = username
            flask_login_user(user)
            return redirect(url_for('inicio'))

        else:
            flash('Usuario o contraseña incorrectos')
            return redirect(url_for('login_page'))


@app.route('/logout') # cierra sesion
@login_required
def logout():
    logout_user()
    return redirect(url_for('inicio'))

@app.route('/')
def inicio():
    return render_template('inicio.html')

 #Fin Flask_Login usuarios
    
@app.route('/productos')
def productos():
    if current_user.is_authenticated:
        cursor = mysql.connection.cursor()
        #JOIN para conseguir los detalles del producto y el nombre del proveedor
        cursor.execute("SELECT p.Codigo, p.Nombre, pr.Nombre, p.Categoria, p.Cantidad, p.Foto, p.Precio FROM productos p JOIN proveedores pr ON p.IdProveedor = pr.CodigoProv")
        productos = cursor.fetchall()
        cursor.close()
        return render_template('productos.html', productos=productos)
    else:
        flash('Por favor inicie sesión para ver esta página')
        return redirect(url_for('login_page'))


@app.route('/agregar_producto', methods=['GET', 'POST'])
def agregar_producto():
    if current_user.is_authenticated:
        if request.method == 'POST':
            nombre = request.form['nombre']
            precio = request.form['precio']
            categoria = request.form['categoria']
            cantidad = request.form['cantidad']
            foto = request.form['foto']
            proveedor = request.form['proveedor']  # para tener el valor seleccionado en el desplegable

            cursor = mysql.connection.cursor()
            cursor.execute("SELECT MAX(codigo) FROM productos")
            max_codigo = cursor.fetchone()[0]  # Obtener el valor máximo
            nuevo_codigo = max_codigo + 1 if max_codigo else 1  # Generar el nuevo código

            # agrega el código de proveedor a la consulta INSERT
            cursor.execute("INSERT INTO productos (codigo, nombre, precio, categoria, cantidad, foto, IdProveedor) VALUES (%s, %s, %s, %s, %s, %s, %s)", (nuevo_codigo, nombre, precio, categoria, cantidad, foto, proveedor))
            mysql.connection.commit()
            cursor.close()
            
            flash('Producto agregado correctamente', 'success')
            return redirect(url_for('productos'))
        else:
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT CodigoProv, Nombre FROM proveedores')
            proveedores = cursor.fetchall()
            cursor.close()
            # renderiza la plantilla y pasa la lista de proveedores como variable
            return render_template('agregar_producto.html', proveedores=proveedores)
    else:
        flash('registrese para ingresar')
        return redirect(url_for('login_page'))


@app.route('/editar_producto/<int:codigo>', methods=['GET', 'POST'])
def editar_producto(codigo):
    if current_user.is_authenticated:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM productos WHERE codigo = %s", (codigo,))
        producto = cursor.fetchone()

        # Conseguir la lista de proveedores
        cursor.execute("SELECT * FROM proveedores")
        proveedores = cursor.fetchall()

        cursor.close()

        if producto is None:
            flash('El producto no existe', 'danger')
            return redirect(url_for('productos'))

        if request.method == 'POST':
            nombre = request.form['nombre']
            precio = request.form['precio']
            categoria = request.form['categoria']
            cantidad = request.form['precio']
            proveedor = request.form['proveedor']

            cursor = mysql.connection.cursor()
            cursor.execute("UPDATE productos SET nombre = %s, precio = %s,IdProveedor  = %s, categoria = %s, cantidad = %s WHERE codigo = %s", (nombre, precio, proveedor, categoria, cantidad, codigo))
            mysql.connection.commit()
            cursor.close()

            flash('Producto actualizado correctamente', 'success')
            return redirect(url_for('productos'))
        else:
            # pasar la lista de proveedores al template
            return render_template('editar_producto.html', producto=producto, proveedores=proveedores)
    else:
        flash('registrese para ingresar')
        return redirect(url_for('login_page'))



@app.route('/eliminar_producto/<int:codigo>', methods=['GET', 'POST'])
def eliminar_producto(codigo):
     if current_user.is_authenticated:

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM productos WHERE codigo = %s", (codigo,))
        producto = cursor.fetchone()
        cursor.close()

        if producto is None:
            flash('El producto no existe', 'danger')
        else:
            cursor = mysql.connection.cursor()
            cursor.execute("DELETE FROM productos WHERE codigo = %s", (codigo,))
            mysql.connection.commit()
            cursor.close()
            flash('Producto eliminado correctamente', 'success')

        return redirect(url_for('productos'))
     else:
        flash('registrese para ingresar')
        return redirect(url_for('login_page'))
    


@app.route('/proveedores')
def proveedores():
    if current_user.is_authenticated:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM proveedores")
        proveedores = cursor.fetchall()
        cursor.close()
        return render_template('proveedores.html', proveedores=proveedores)
    

@app.route('/agregar_proveedor', methods=['GET', 'POST'])
def agregar_proveedor():
    if current_user.is_authenticated:
        if request.method == 'POST':
            nombre = request.form['nombre']
            direccion = request.form['direccion']
            cel = request.form['cel']
            email = request.form['email']

            cursor = mysql.connection.cursor()
            cursor.execute("SELECT MAX(CodigoProv) FROM proveedores")
            max_codigo = cursor.fetchone()[0]  # Obtener el valor máximo
            nuevo_codigo = max_codigo + 1 if max_codigo else 1  # Generar el nuevo código

            cursor.execute("INSERT INTO proveedores (CodigoProv, Nombre, Direccion, cel, Email) VALUES (%s, %s, %s, %s, %s)", (nuevo_codigo, nombre, direccion, cel, email))
            mysql.connection.commit()
            cursor.close()

            flash('Proveedor agregado correctamente', 'success')
            return redirect(url_for('proveedores'))
        else:
            return render_template('agregar_proveedor.html')
    else:
        return redirect(url_for('login_page'))
    
    
@app.route('/editar_proveedor/<int:codigo>', methods=['GET', 'POST'])
def editar_proveedor(codigo):
    if current_user.is_authenticated:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM proveedores WHERE CodigoProv = %s", (codigo,))
        proveedor = cursor.fetchone()
        cursor.close()

        if proveedor is None:
            flash('El proveedor no existe', 'danger')
            return redirect(url_for('proveedores'))

        if request.method == 'POST':
            nombre = request.form['nombre']
            direccion = request.form['direccion']
            cel = request.form['cel']
            email = request.form['email']

            cursor = mysql.connection.cursor()
            cursor.execute("UPDATE proveedores SET nombre = %s, direccion = %s, cel = %s, email = %s WHERE CodigoProv = %s", (nombre, direccion, cel, email, codigo))
            mysql.connection.commit()
            cursor.close()

            flash('Proveedor actualizado correctamente', 'success')
            return redirect(url_for('proveedores'))
        else:
            return render_template('editar_proveedor.html', proveedor=proveedor)
    else:
        return redirect(url_for('login_page'))
    


@app.route('/eliminar_proveedor/<int:codigo>', methods=['GET', 'POST'])
def eliminar_proveedor(codigo):
    if current_user.is_authenticated:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM proveedores WHERE CodigoProv = %s", (codigo,))
        proveedor = cursor.fetchone()

        if proveedor is None:
            flash('El proveedor no existe', 'danger')
        else:
            # Verificar si el proveedor tiene productos asociados
            cursor.execute("SELECT * FROM productos WHERE IdProveedor = %s", (codigo,))
            producto = cursor.fetchone()

            if producto is not None:
                # El proveedor tiene productos asociados
                flash('No se puede eliminar este proveedor porque aún tiene productos asociados', 'warning')
            else:
                # El proveedor no tiene productos asociados
                cursor.execute("DELETE FROM proveedores WHERE CodigoProv = %s", (codigo,))
                mysql.connection.commit()
                flash('Proveedor eliminado correctamente', 'success')

        cursor.close()
        return redirect(url_for('proveedores'))
    else:
        return redirect(url_for('login_page'))
    

@app.route('/ventas')
def ventas():
    if current_user.is_authenticated:
        carro = session.get('carro', [])        

        # Calcula la cantidad total de productos en el carrito
        total_cantidad = sum(item['Cantidad'] for item in carro)

        # Calcula el precio total de los productos en el carrito
        total_precio = sum(item['Precio'] * item['Cantidad'] for item in carro)

        return render_template('ventas.html', carro=carro, total_cantidad=total_cantidad, total_precio=total_precio)
    else:
        flash('registrese para ingresar')
        return redirect(url_for('login_page'))
   

    

@app.route('/agregar_al_carro/<int:Codigo>', methods=['POST'])
def agregar_al_carro(Codigo):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT p.Codigo, p.Nombre, pr.Nombre, p.Categoria, p.Cantidad, p.Foto, p.Precio FROM productos p JOIN proveedores pr ON p.IdProveedor = pr.CodigoProv WHERE p.Codigo = %s', (Codigo,))
    producto = cursor.fetchone()

    Cantidad = int(request.form.get('Cantidad'))

    # Actualizar la cantidad de productos disponibles en la base de datos para no poder agregar mas productos de los disponibles
    nueva_cantidad = producto[4] - Cantidad
    cursor.execute('UPDATE productos SET Cantidad = %s WHERE Codigo = %s', (nueva_cantidad, Codigo))
    mysql.connection.commit()

    # En caso de que el carrito no exista
    if 'carro' not in session:
        session['carro'] = []

    # Verificar si el producto ya esta en el carrito
    encontre = False
    for item in session['carro']:
        if item['Codigo'] == producto[0]:
            item['Cantidad'] += Cantidad
            encontre = True
            break

    # Si el producto no está en el carrito agregarlo
    if not encontre:
        session['carro'].append({
            'Codigo': producto[0],
            'Nombre': producto[1],
            'Proveedor': producto[2],  # Agregar el nombre del proveedor al carrito
            'Precio': producto[6],
            'Cantidad': Cantidad,
            'Foto': producto[5]  # Agregar la imagen del producto al carrito
        })

    # Guarda los cambios en la sesion
    session.modified = True

    cursor.close()

    return redirect(url_for('ventas'))


@app.route('/eliminar_del_carro/<int:Codigo>', methods=['POST'])
def eliminar_del_carro(Codigo):
    cursor = mysql.connection.cursor()
    
    # Obtener la cantidad de productos a devolver al stock
    Cantidad = int(request.form.get('Cantidad'))

    # Actualizar la cantidad de productos disponibles en la base de datos
    cursor.execute('UPDATE productos SET Cantidad = Cantidad + %s WHERE Codigo = %s', (Cantidad, Codigo))
    mysql.connection.commit()

    # Actualizar la cantidad de productos en el carrito
    for item in session['carro']:
        if item['Codigo'] == Codigo:
            item['Cantidad'] -= Cantidad
            if item['Cantidad'] <= 0:
                # Eliminar el producto del carrito si su cantidad es cero o negativa
                session['carro'].remove(item)
            break

    # Guarda los cambios en la sesion
    session.modified = True
    cursor.close()
    return redirect(url_for('ventas'))


if __name__ == '__main__':
    app.secret_key = 'secret_key'
    app.run(debug=True)
