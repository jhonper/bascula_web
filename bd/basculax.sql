use basculax;

-- Tabla Productos 
CREATE TABLE Productos ( 
    IDproducto INT AUTO_INCREMENT PRIMARY KEY, 
    Codigo VARCHAR(50), 
    Nombre VARCHAR(255) 
); 

INSERT INTO Productos (Codigo, Nombre) 
VALUES 
('1', 'PROD-001'), 
('2', 'PROD-002'), 
('3', 'PROD-003'), 
('4', 'PROD-004'), 
('5', 'PROD-005'), 
('6', 'PROD-006'), 
('7', 'PROD-007'), 
('8', 'PROD-008'), 
('9', 'PROD-009'), 
('9', 'PROD-010');
-- 

CREATE TABLE Vehiculo( 
  id INT AUTO_INCREMENT PRIMARY KEY, 
    placa VARCHAR(10), 
    nombre VARCHAR(255) 
); 
use basculax;
select * from origenes;
select * from destinos;
select * from Movimiento; 
select * from Vehiculo;
select * from conductores;
select * from user;
select * from proveedores;
select * from productos;
use basculax;


SELECT Movimiento.idmovimiento, Movimiento.fechaentrada, Movimiento.horaentrada, Movimiento.observaciones,
                            Proveedores.documento AS documentoproveedor, Proveedores.nombre AS nombreproveedor, Movimiento.pesoentrada,
                            Movimiento.pesosalida, Movimiento.pesoneto,
                            Conductores.nombre AS nombreconductor,
                            Vehiculo.placa AS placa,
                            Productos.codigo AS codigoproducto, Productos.nombre AS nombreproducto,
                            Origenes.codigo AS codigoorigen, Origenes.origen AS origen, 
                            Destinos.codigo AS codigodestino, Destinos.destino AS destino
                            FROM Movimiento
                            INNER JOIN Proveedores ON Movimiento.idproveedor = Proveedores.id 
                            JOIN Conductores ON Movimiento.idconductor = Conductores.id 
                            JOIN Productos ON Movimiento.idproducto = Productos.IDproducto
                            JOIN Origenes ON Movimiento.idorigen = Origenes.idorigen
                            JOIN Destinos ON Movimiento.iddestino = Destinos.iddestino
                            JOIN Vehiculo ON Movimiento.idvehiculo = Vehiculo.id
                          -- WHERE Proveedores.documento = 12345678;  
                        WHERE fechaentrada BETWEEN '2024-03-22' AND '2024-03-26' AND fechasalida IS NOT NULL AND Proveedores.documento = '';
-- **********************************************************************************************
SELECT Movimiento.idmovimiento, Movimiento.tipomovimiento, Movimiento.fechaentrada, Movimiento.horaentrada, Movimiento.fechasalida, Movimiento.horasalida,
                            Movimiento.observaciones,
                            Proveedores.documento AS documentoproveedor, Proveedores.nombre AS nombreproveedor, 
                            Movimiento.pesoentrada, Movimiento.pesosalida, Movimiento.pesoneto,
                            Conductores.nombre AS nombreconductor,
                            Vehiculo.placa AS placa,
                            Productos.codigo AS codigoproducto, Productos.nombre AS nombreproducto,
                            Origenes.codigo AS codigoorigen, Origenes.origen AS origen, 
                            Destinos.codigo AS codigodestino, Destinos.destino AS destino
                            FROM Movimiento
                            INNER JOIN Proveedores ON Movimiento.idproveedor = Proveedores.id 
                            JOIN Conductores ON Movimiento.idconductor = Conductores.id 
                            JOIN Productos ON Movimiento.idproducto = Productos.IDproducto
                            JOIN Origenes ON Movimiento.idorigen = Origenes.idorigen
                            JOIN Destinos ON Movimiento.iddestino = Destinos.iddestino
                            JOIN Vehiculo ON Movimiento.idvehiculo = Vehiculo.id
                            where Proveedores.documento = 12345678 AND tipomovimiento = 'E' and Productos.nombre = 'PROD-001';
                            
                          
-- 
-- update movimiento set tipomovimiento = 'E' where idmovimiento=6;
use basculax;

select * from movimiento;
select * from origenes;
select * from destinos;
select * from productos;
select * from vehiculo;
select * from user;
-- update user set username; 
select * from conductores;
select * from proveedores;
select * from user where id = 13;
-- update user set codigoprov = '7575' where id = 4
insert into user
-- update user set  = 1 where id = 1;
-- update user set editarpesos = 1 where id = True;
-- update user set productospermitidos = '1,2,3,4,5,6,7,8,9' where id = 1;


-- update proveedores set nombre = 'Cliente A' where id = 1;
-- update proveedores set nombre = 'Cliente B' where id = 2;
-- update proveedores set nombre = 'Cliente C' where id = 3;
-- update proveedores set nombre = 'Cliente D' where id = 4;
-- update proveedores set nombre = 'Cliente E' where id = 5;
-- update proveedores set nombre = 'Cliente F' where id = 6;
-- update proveedores set nombre = 'Cliente G' where id = 7;
-- update proveedores set nombre = 'Cliente H' where id = 8;
-- update proveedores set nombre = 'Cliente I' where id = 9;
-- update proveedores set nombre = 'Cliente J' where id = 10;
update movimiento set tipomovimiento = "E" where idmovimiento = 7;

select * from proveedores;

-- update user set codigoprov = null where id = 1;
-- update user set productospermitidos = "1,2,8" where id=13;
-- update user set username = "Operario9" where id=13;
select * from user;
select * from proveedores;
select * from productos;
 CREATE TABLE Movimiento ( 
    idmovimiento INT AUTO_INCREMENT PRIMARY KEY, 
    idproveedor INT,
    idconductor INT,
    idvehiculo INT,
    idproducto INT, 
    idorigen INT,
    iddestino INT,
    observaciones VARCHAR(255), 
    fechaentrada DATE,
    horaentrada TIME, 
    fechasalida DATE, 
    horasalida TIME, 
    pesoentrada INT, 
    pesosalida INT, 
    pesoneto INT, 
    idoperario INT, 
    idbascula INT,
    idbodega INT,
    FOREIGN KEY (idproveedor) REFERENCES proveedores (id),
    FOREIGN KEY (idconductor) REFERENCES conductores (id),
    FOREIGN KEY (idvehiculo) REFERENCES vehiculo (id),
    FOREIGN KEY (idproducto) REFERENCES productos (IDproducto), 
    FOREIGN KEY (idorigen) REFERENCES origenes (idorigen),
    FOREIGN KEY (iddestino) REFERENCES destinos (iddestino),
    FOREIGN KEY (idoperario) REFERENCES operarios (idoperario), 
    FOREIGN KEY (idbascula) REFERENCES basculas (Idbascula), 
    FOREIGN KEY (idbodega) REFERENCES bodegas (idBodega)
); 

-- ALTER TABLE Movimiento
-- ADD COLUMN idusuario INT,
-- ADD FOREIGN KEY (idusuario) REFERENCES user(id);

-- ALTER TABLE Movimiento
-- ADD COLUMN tipomovimiento varchar(10);
-- ADD FOREIGN KEY (idusuario) REFERENCES user(id);
use basculax;

select * from user;
select * from user where editarpesos is NULL; 
select * from productos;
-- ALTER TABLE user
-- ADD COLUMN editarpesos BOOLEAN;
-- ALTER TABLE user
-- ADD COLUMN productospermitidos varchar(250);

CREATE TABLE `user` (
  `id` smallint(3) AUTO_INCREMENT PRIMARY KEY,
  `username` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `password` char(102) COLLATE utf8_unicode_ci NOT NULL,
  `descripcion` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `codigoprov` varchar(50) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='Stores the user''s data.';

create database flask_login;
use flask_login;
CREATE TABLE user( 
  id INT AUTO_INCREMENT PRIMARY KEY, 
  username VARCHAR(10), 
  password VARCHAR(255), 
  fullname VARCHAR(255)
); 
use basculax;
CREATE TABLE user( 
  id INT AUTO_INCREMENT PRIMARY KEY, 
  username VARCHAR(10), 
  password VARCHAR(255), 
  descripcion VARCHAR(255),
  codigoprov VARCHAR(255)
); 
select * from user

-- ALTER TABLE user
-- MODIFY username VARCHAR(50);

INSERT INTO user (username, password, fullname) VALUES
('admin', 'scrypt:32768:8:1$JU04rTXz2nYHr2uo$7278ab1f6397868cec19877effc316effdeb9938f08cdac2d11b52eeedc6d2ca7053e6d2baf9cfac60c113bebfc4c4aa9c5e5954215107bedd9c481b5dad1db7', 'administrador'),
('operario', '12345', 'operario'),
('prov', '12345', 'proveedor');






INSERT INTO user (username, password, fullname) VALUES
('admin', 'scrypt:32768:8:1$JU04rTXz2nYHr2uo$7278ab1f6397868cec19877effc316effdeb9938f08cdac2d11b52eeedc6d2ca7053e6d2baf9cfac60c113bebfc4c4aa9c5e5954215107bedd9c481b5dad1db7', 'administrador'),
('operario', 'scrypt:32768:8:1$JU04rTXz2nYHr2uo$7278ab1f6397868cec19877effc316effdeb9938f08cdac2d11b52eeedc6d2ca7053e6d2baf9cfac60c113bebfc4c4aa9c5e5954215107bedd9c481b5dad1db7', 'operario'),
('prov', 'scrypt:32768:8:1$JU04rTXz2nYHr2uo$7278ab1f6397868cec19877effc316effdeb9938f08cdac2d11b52eeedc6d2ca7053e6d2baf9cfac60c113bebfc4c4aa9c5e5954215107bedd9c481b5dad1db7', 'proveedor');

INSERT INTO user (username, password, descripcion, codigoprov) VALUES
('admin', 'scrypt:32768:8:1$JU04rTXz2nYHr2uo$7278ab1f6397868cec19877effc316effdeb9938f08cdac2d11b52eeedc6d2ca7053e6d2baf9cfac60c113bebfc4c4aa9c5e5954215107bedd9c481b5dad1db7', 'administrador',''),
('operario', 'scrypt:32768:8:1$JU04rTXz2nYHr2uo$7278ab1f6397868cec19877effc316effdeb9938f08cdac2d11b52eeedc6d2ca7053e6d2baf9cfac60c113bebfc4c4aa9c5e5954215107bedd9c481b5dad1db7', 'operario',''),
('prov', 'scrypt:32768:8:1$JU04rTXz2nYHr2uo$7278ab1f6397868cec19877effc316effdeb9938f08cdac2d11b52eeedc6d2ca7053e6d2baf9cfac60c113bebfc4c4aa9c5e5954215107bedd9c481b5dad1db7', 'proveedor','1');



