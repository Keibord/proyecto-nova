# Proyecto Nova

## Descripción

Una aplicación web para el uso de la empresa Nova. Este proyecto es un proyecto de aprendizaje con el objetivo de crear una aplicación web para el uso de la empresa Nova, una empresa dedicada a la venta de productos electrónicos. El proyecto intenta realizar una página para el control de stock de productos y de proveedores de la empresa, una interfaz para la venta de productos por parte de los empleados con un control de usuarios y con generación de tickets. El proyecto se utilizaría desde una página web hosteada con Python y Flask y sería accesible desde cualquier sitio mientras se posea de conexión a internet.

## Instalación

Para instalar y ejecutar este proyecto, se requieren los siguientes pasos:

1. Clonar o descargar el repositorio de github 
2. Instalar Python 3.9 o superior 
3. Instalar las dependencias del proyecto usando el comando `pip install -r requirements.txt` en la carpeta del proyecto.
4. Configurar las variables de entorno necesarias para el proyecto, como la cadena de conexión a la base de datos, el nombre del administrador y la contraseña.
5. Ejecutar el archivo `Nova.py` usando el comando `python Nova.py` en la carpeta del proyecto.
6. Abrir un navegador web y acceder a la dirección `http://localhost:5000` para ver la aplicación.

## Uso

Para usar este proyecto, se deben seguir los siguientes pasos:

1. Iniciar sesión con un usuario y una contraseña válidos.
2. Navegar por las diferentes opciones del menú principal, según el rol del usuario. Los roles disponibles son: administrador y empleado .
    - El administrador puede gestionar los productos, los proveedores y los empleados.
    - El empleado puede vender productos a los clientes y generar tickets.
