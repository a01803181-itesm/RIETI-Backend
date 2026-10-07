-- SQLBook: Code
drop database if exists RIETI;
create database RIETI;

use RIETI;

drop table if exists Expediente;
drop table if exists AdminReporte;
drop table if exists Reporte;
drop table if exists Alimentador;
drop table if exists Admin;
drop table if exists Usuario;
drop table if exists Evidencia;

create table Usuario(
correoU varchar(100) primary key,
proveedor enum('cognito', 'google') not null
);

create table Admin(
correoAd varchar(100) primary key,
proveedor enum('cognito', 'google') not null,
nombre varchar(50) not null,
ap_paterno varchar(64) not null, 
ap_materno varchar(64) not null, 
telefono varchar(10) not null
);

create table Alimentador(
correoAl varchar(100) primary key,
proveedor enum('cognito', 'google') not null,
telefono varchar(10) not null,
nombre varchar(50) not null,
ap_paterno varchar(64) not null, 
ap_materno varchar(64) not null, 
municipio varchar(30) not null
);

create table Expediente(
folioE varchar(32) primary key,
lugar varchar(32) not null,
descripcion varchar(100), 
estatus enum('1_Registrado','2_En_revision','3_En_seguimiento', '4_Canalizado',
'5_Concluido', '6_Archivado', '7_Cancelado','8_Reincidente') default '1_Registrado' not null,
correoAl varchar(100),
foreign key (correoAl) references Alimentador(correoAl) on delete cascade
);

create table Reporte(
folio varchar(32) primary key,
edad enum ('INFANTES', 'PUBERTOS', 'JOVENES', 'MIXTO'),
dia timestamp not null,
tipoTrabajo enum ('VENTA_AMBULANTE', 'LIMPIEZA_DE_PARABRISAS', 'MENDICIDAD', 'CARGA_Y_DESCARGA', 'TRABAJO_EN_COMERCIO', 'CAMPO', 'CONSTRUCCION','TRABAJO_DOMESTICO','RECOLECCION_DE_RESIDUOS', 'OTRA_ACTIVIDAD'),
numNinios int(3),
direccion varchar(100) not null,
municipio enum ('ATIZAPAN', 'NAUCALPAN', 'CUAUTITLAN_IZCALLI', 'CUAUTITLAN', 
'HUIXQUILUCAN', 'NICOLAS_ROMERO', 'TLALNEPANTLA', 'TULTITLAN', 'COACALCO', 'ECATEPEC', 'NEZAHUALCOYOTL'),
latitud DECIMAL(9,6) not null,
longitud DECIMAL(9,6) not null, 
nombre varchar(50) not null,
ap_paterno varchar(64) not null, 
ap_materno varchar(64) not null, 
detalles_adcionales text,
correoU varchar(100),
folioE varchar(32),
correoAl varchar(100),
foreign key (correoU) references Usuario(correoU) on delete cascade,
foreign key (folioE) references Expediente(folioE) on delete cascade,
foreign key (correoAl) references Alimentador(correoAl) on delete cascade
);

create table AdminReporte(
correoAd varchar(100),
folio varchar(32),
descripcion text, 
primary key (correoAd, folio),
foreign key(correoAd) references Admin(correoAd),
foreign key (folio) references Reporte(folio)
);

create table Evidencia(
id int auto_increment primary key,
url varchar(255) not null,
folio varchar(32),
foreign key (folio) references Reporte(folio)
);

INSERT INTO Usuario (correoU, contrasenia, proveedor) VALUES
("casita@gmail.com", "123456", "local")