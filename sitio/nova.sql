-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 06-06-2023 a las 04:26:55
-- Versión del servidor: 10.4.13-MariaDB
-- Versión de PHP: 7.4.7

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `nova`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cliente`
--

CREATE TABLE `cliente` (
  `idCuil` int(11) NOT NULL,
  `Nombre` varchar(20) COLLATE utf8mb4_spanish_ci NOT NULL,
  `Apellido` varchar(20) COLLATE utf8mb4_spanish_ci NOT NULL,
  `TipoConsumidor` varchar(50) COLLATE utf8mb4_spanish_ci NOT NULL,
  `Cel` varchar(20) COLLATE utf8mb4_spanish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle`
--

CREATE TABLE `detalle` (
  `idDetalle` int(11) NOT NULL,
  `idProducto` int(11) NOT NULL,
  `Cantidad` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `factura`
--

CREATE TABLE `factura` (
  `CodigoFac` int(3) NOT NULL,
  `idDetalle` int(8) NOT NULL,
  `idCliente` int(20) NOT NULL,
  `Fecha` date NOT NULL,
  `Subtotal` double NOT NULL,
  `Total` double NOT NULL,
  `Impuestos` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `Codigo` int(3) NOT NULL,
  `Nombre` varchar(30) COLLATE utf8mb4_spanish_ci NOT NULL,
  `IdProveedor` int(2) NOT NULL,
  `Categoria` varchar(30) COLLATE utf8mb4_spanish_ci NOT NULL,
  `Cantidad` int(3) NOT NULL,
  `Foto` varchar(100) COLLATE utf8mb4_spanish_ci NOT NULL,
  `Precio` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`Codigo`, `Nombre`, `IdProveedor`, `Categoria`, `Cantidad`, `Foto`, `Precio`) VALUES
(1, 'Cable miniusb', 0, 'Cable ', 4, 'static/imagenes/0.jpeg', 2500),
(2, 'Auriculares Pioneer', 0, 'Auriculares', 1, 'static/imagenes/1.jpg', 4200),
(3, 'Auriculares Bluetooth XPODS', 0, 'Auriculares', 1, 'static/imagenes/2.jpg', 10850),
(4, 'Tarjeta SD 4gb', 0, 'Tarjeta de Memoria', 4, 'static/imagenes/4.jpg', 1400);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proveedores`
--

CREATE TABLE `proveedores` (
  `CodigoProv` int(2) NOT NULL,
  `Nombre` varchar(20) COLLATE utf8mb4_spanish_ci NOT NULL,
  `Direccion` varchar(40) COLLATE utf8mb4_spanish_ci NOT NULL,
  `Cel` varchar(20) COLLATE utf8mb4_spanish_ci NOT NULL,
  `Email` varchar(60) COLLATE utf8mb4_spanish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `proveedores`
--

INSERT INTO `proveedores` (`CodigoProv`, `Nombre`, `Direccion`, `Cel`, `Email`) VALUES
(0, 'Panda', 'Chile 150', '2914525547', 'pandatecno@gmail.com');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
-- 1 admin - 2 empleado - 3 cliente

CREATE TABLE `usuario` (
  `User` varchar(20) COLLATE utf8mb4_spanish_ci NOT NULL,
  `Password` varchar(200) COLLATE utf8mb4_spanish_ci NOT NULL,
  `TipoUser` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`User`, `Password`, `TipoUser`) VALUES
('Marcos', '$2y$10$uMU2Trl/A65NMXBDqEr/8OpHvnRB0Rw0PXNJzYlirp/3noevWjZyu', 1),
('Mati', '$2y$10$dwulA/rhclEHK.jDXt128.4sGR.EAWkjwUOIKSfCIIuKIB3DqI/2m', 1);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `cliente`
--
ALTER TABLE `cliente`
  ADD PRIMARY KEY (`idCuil`);

--
-- Indices de la tabla `detalle`
--
ALTER TABLE `detalle`
  ADD PRIMARY KEY (`idDetalle`),
  ADD KEY `idProducto` (`idProducto`);

--
-- Indices de la tabla `factura`
--
ALTER TABLE `factura`
  ADD PRIMARY KEY (`CodigoFac`),
  ADD KEY `idDetalle` (`idDetalle`),
  ADD KEY `idCliente` (`idCliente`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`Codigo`),
  ADD KEY `IdProveedor` (`IdProveedor`);

--
-- Indices de la tabla `proveedores`
--
ALTER TABLE `proveedores`
  ADD PRIMARY KEY (`CodigoProv`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`User`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `Codigo` int(3) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `cliente`
--
ALTER TABLE `cliente`
  ADD CONSTRAINT `cliente_ibfk_1` FOREIGN KEY (`idCuil`) REFERENCES `factura` (`idCliente`);

--
-- Filtros para la tabla `detalle`
--
ALTER TABLE `detalle`
  ADD CONSTRAINT `detalle_ibfk_1` FOREIGN KEY (`idProducto`) REFERENCES `productos` (`Codigo`);

--
-- Filtros para la tabla `factura`
--
ALTER TABLE `factura`
  ADD CONSTRAINT `factura_ibfk_1` FOREIGN KEY (`idDetalle`) REFERENCES `detalle` (`idDetalle`);

--
-- Filtros para la tabla `productos`
--
ALTER TABLE `productos`
  ADD CONSTRAINT `productos_ibfk_2` FOREIGN KEY (`IdProveedor`) REFERENCES `proveedores` (`CodigoProv`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
