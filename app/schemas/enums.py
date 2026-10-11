"""Módulo de enumeraciones y catálogos estandarizados del dominio RIETI.

Define los tipos enumerados para proveedores de autenticación, estatus de expedientes,
rangos de edad observados y tipologías de trabajo infantil.
"""

from enum import Enum

class Provider(Enum):
    """Proveedores de autenticación e identidad federada admitidos en el sistema.

    Attributes:
        COGNITO: Autenticación mediante AWS Cognito User Pool.
        GOOGLE: Autenticación federada mediante proveedor Google OAuth.
    """
    COGNITO = 'cognito'
    GOOGLE = 'google'


class Status(str, Enum):
    """Ciclo de vida y estados administrativos de los reportes y expedientes.

    Attributes:
        REGISTRADO: Reporte recién ingresado por el ciudadano.
        EN_REVISION: Reporte en validación inicial por personal administrativo.
        EN_SEGUIMIENTO: Expediente en proceso de investigación y visitas de campo.
        CANALIZADO: Expediente derivado a instancias o dependencias gubernamentales competentes.
        CONCLUIDO: Caso finalizado y resuelto.
        ARCHIVADO: Caso cerrado sin acción posterior requerida.
        CANCELADO: Reporte descartado por duplicidad, falsedad o error.
        REINCIDENTE: Detección reiterada en una misma ubicación o menores identificados previamente.
    """
    REGISTRADO = '1_Registrado'
    EN_REVISION = '2_En_revision'
    EN_SEGUIMIENTO = '3_En_seguimiento'
    CANALIZADO = '4_Canalizado'
    CONCLUIDO = '5_Concluido'
    ARCHIVADO = '6_Archivado'
    CANCELADO = '7_Cancelado'
    REINCIDENTE = '8_Reincidente'

class RangoEdad(Enum):
    """Rangos etarios estimados para clasificar a los menores identificados en reportes.

    Attributes:
        INFANTES: Primera infancia y niñez temprana (0 a 11 años).
        PUBERTOS: Adolescencia inicial o pubertad (12 a 14 años).
        JOVENES: Adolescentes de 15 a 17 años en edad permitida/no permitida sujeta a regulación.
        MIXTO: Grupo observado integrado por menores de distintos rangos de edad.
    """
    INFANTES = 'INFANTES'
    PUBERTOS = 'PUBERTOS'
    JOVENES = 'JOVENES'
    MIXTO = 'MIXTO'

class TipoTrabajo(Enum):
    """Tipologías y clasificaciones operativas de trabajo infantil o actividades en vía pública.

    Attributes:
        VENTA_AMBULANTE: Comercialización informal de productos en cruceros o calles.
        LIMPIEZA_DE_PARABRISAS: Limpieza vehicular en semáforos o paradas de transporte.
        MENDICIDAD: Petición de limosna o dinero en vía pública.
        CARGA_Y_DESCARGA: Trabajos de esfuerzo físico pesado en mercados o centrales de abasto.
        TRABAJO_EN_COMERCIO: Empleo subordinado o familiar en locales comerciales.
        CAMPO: Labores agrícolas o pecuarias en zonas rurales.
        CONSTRUCCION: Apoyo en obras o albañilería.
        TRABAJO_DOMESTICO: Labores de hogar intensivas sin escolarización.
        RECOLECCION_DE_RESIDUOS: Pepena o recolección de materiales reciclables y basura.
        OTRA_ACTIVIDAD: Otras actividades no tipificadas en los rubros principales.
    """
    VENTA_AMBULANTE = 'VENTA_AMBULANTE'
    LIMPIEZA_DE_PARABRISAS = 'LIMPIEZA_DE_PARABRISAS'
    MENDICIDAD = 'MENDICIDAD'
    CARGA_Y_DESCARGA = 'CARGA_Y_DESCARGA'
    TRABAJO_EN_COMERCIO = 'TRABAJO_EN_COMERCIO'
    CAMPO = 'CAMPO'
    CONSTRUCCION = 'CONSTRUCCION'
    TRABAJO_DOMESTICO = 'TRABAJO_DOMESTICO'
    RECOLECCION_DE_RESIDUOS = 'RECOLECCION_DE_RESIDUOS'
    OTRA_ACTIVIDAD = 'OTRA_ACTIVIDAD'