from enum import Enum

class Provider(Enum):
    COGNITO = 'cognito'
    GOOGLE = 'google'


class Status(str, Enum):
    REGISTRADO = '1_Registrado'
    EN_REVISION = '2_En_revision'
    EN_SEGUIMIENTO = '3_En_seguimiento'
    CANALIZADO = '4_Canalizado'
    CONCLUIDO = '5_Concluido'
    ARCHIVADO = '6_Archivado'
    CANCELADO = '7_Cancelado'
    REINCIDENTE = '8_Reincidente'

class RangoEdad(Enum):
    INFANTES = 'INFANTES'
    PUBERTOS = 'PUBERTOS'
    JOVENES = 'JOVENES'
    MIXTO = 'MIXTO'

class TipoTrabajo(Enum):
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