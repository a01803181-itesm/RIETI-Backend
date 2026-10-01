from enum import Enum

class Provider(Enum):
    LOCAL = 'local'
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
    
class MunicipioEnum(str, Enum):
    ATIZAPAN = " ATIZAPAN"
    NAUCALPAN = "NAUCALPAN"
    CUAUTITLAN_IZCALLI = "CUAUTITLAN_IZCALLI"
    CUAUTITLAN = "CUAUTITLAN"
    HUIXQUILUCAN = "HUIXQUILUCAN"
    NICOLAS_ROMERO = "NICOLAS_ROMERO"
    TLALNEPANTLA = "TLALNEPANTLA"
    TULTITLAN = "TULTITLAN"
    COACALCO = "COACALCO"
    ECATEPEC = "ECATEPEC"
    NEZAHUALCOYOTL = "NEZAHUALCOYOTL"