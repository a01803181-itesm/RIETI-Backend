"""Módulo de esquemas Pydantic para reportes ciudadanos, geolocalización y métricas estadísticas."""

from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from pydantic_extra_types.coordinate import Latitude, Longitude
from app.schemas.enums import RangoEdad, TipoTrabajo

class Reporte(BaseModel):
    """Modelo principal de reporte ciudadano sobre presunto caso de trabajo infantil.

    Attributes:
        folio (str): Código alfanumérico identificador único del reporte.
        edad (RangoEdad): Grupo etario en el que se ubican los menores observados.
        dia (datetime): Fecha y hora en que se suscitó o registró el incidente.
        tipoTrabajo (TipoTrabajo): Categoría o tipología de la actividad identificada.
        numNinios (int | None): Número estimado de menores en situación de trabajo.
        direccion (str): Dirección exacta o referencias del punto geográfico.
        municipio (str): Municipio donde se levantó la observación.
        latitud (Latitude): Coordenada geográfica de latitud (-90 a 90).
        longitud (Longitude): Coordenada geográfica de longitud (-180 a 180).
        nombre (str | None): Nombre del denunciante (opcional).
        ap_paterno (str | None): Primer apellido del denunciante (opcional).
        ap_materno (str | None): Segundo apellido del denunciante (opcional).
        detalles_adcionales (str | None): Información complementaria o señas particulares.
        correoU (EmailStr): Correo electrónico del usuario ciudadano que reporta.
        folioE (str | None): Folio del expediente vinculado si ya fue canalizado.
        correoAl (EmailStr | None): Correo del alimentador o autoridad asignada.
    """
    folio: str = Field(
        ...,
        description="Código alfanumérico identificador único del reporte.",
        examples=["REP-2026-TOL-001"]
    )
    edad: RangoEdad = Field(
        ...,
        description="Rango de edad aproximado de los infantes identificados."
    )
    dia: datetime = Field(
        ...,
        description="Fecha y hora de ocurrencia o registro del incidente.",
        examples=["2026-10-10T14:30:00Z"]
    )
    tipoTrabajo: TipoTrabajo = Field(
        ...,
        description="Tipología o categoría de actividad de trabajo infantil detectada."
    )
    numNinios: int | None = Field(
        default=None,
        description="Cantidad aproximada de infantes involucrados en la escena observada.",
        ge=0,
        examples=[2]
    )
    direccion: str = Field(
        ...,
        description="Ubicación textual, calle, crucero o referencias del avistamiento.",
        examples=["Av. Paseo Tollocan y Comonfort, Semáforo norte"]
    )
    municipio: str = Field(
        ...,
        description="Municipio en el cual se observó la situación.",
        examples=["Toluca"]
    )
    latitud: Latitude = Field(
        ...,
        description="Coordenada geográfica de latitud (-90 a 90 grados).",
        examples=[19.2826]
    )
    longitud: Longitude = Field(
        ...,
        description="Coordenada geográfica de longitud (-180 a 180 grados).",
        examples=[-99.6557]
    )
    nombre: str | None = Field(
        default=None,
        description="Nombre(s) del ciudadano denunciante (opcional para mantener anonimato).",
        examples=["Juan"]
    )
    ap_paterno: str | None = Field(
        default=None,
        description="Primer apellido del denunciante (opcional).",
        examples=["Hernández"]
    )
    ap_materno: str | None = Field(
        default=None,
        description="Segundo apellido del denunciante (opcional).",
        examples=["López"]
    )
    detalles_adcionales: str | None = Field(
        default=None,
        description="Detalles adicionales, señas particulares o contexto relevante.",
        examples=["Venden dulces en el camellón central entre las 12:00 y las 16:00 horas."]
    )
    correoU: EmailStr = Field(
        ...,
        description="Correo del usuario ciudadano que emite el reporte.",
        examples=["ciudadano.activo@gmail.com"]
    )
    folioE: str | None = Field(
        default=None,
        description="Folio del expediente administrativo asignado si ya fue canalizado.",
        examples=["EXP-2026-TOL-042"]
    )
    correoAl: EmailStr | None = Field(
        default=None,
        description="Correo institucional de la autoridad o alimentador que da seguimiento.",
        examples=["alimentador.toluca@rieti.org"]
    )

class CoordenadaReporte(BaseModel):
    """Par de coordenadas geográficas simplificadas para renderizado cartográfico y mapas de calor.

    Attributes:
        lat (float): Latitud en notación decimal.
        lng (float): Longitud en notación decimal.
    """
    lat: float = Field(
        ...,
        description="Coordenada de latitud en grados decimales.",
        examples=[19.2826]
    )
    lng: float = Field(
        ...,
        description="Coordenada de longitud en grados decimales.",
        examples=[-99.6557]
    )

class CategoriaTotal(BaseModel):
    """Estructura clave-valor para agregaciones estadísticas agrupadas por dimensión.

    Attributes:
        categoria (str): Nombre de la etiqueta, mes, municipio, estatus o autoridad.
        total (int): Cantidad acumulada de reportes para dicha categoría.
    """
    categoria: str = Field(
        ...,
        description="Nombre descriptivo de la agrupación (ej. mes, municipio, estatus, hora).",
        examples=["Toluca"]
    )
    total: int = Field(
        ...,
        description="Cantidad total de reportes cuantificados en la categoría.",
        ge=0,
        examples=[45]
    )

class Data(BaseModel):
    """Envoltorio genérico para retornos que constan de un valor numérico decimal.

    Attributes:
        data (float): Valor de punto flotante correspondiente a un promedio o porcentaje.
    """
    data: float = Field(
        ...,
        description="Métrica numérica calculada de punto flotante (porcentaje o promedio).",
        examples=[64.5]
    )

class DataInt(BaseModel):
    """Envoltorio genérico para retornos que constan de un valor numérico entero.

    Attributes:
        data (int): Valor entero representativo de un conteo o magnitud directa.
    """
    data: int = Field(
        ...,
        description="Métrica numérica entera representativa de un conteo.",
        examples=[18]
    )

class DashboardData(BaseModel):
    """Conjunto consolidado de indicadores clave de rendimiento (KPIs) para tableros de control.

    Attributes:
        promedioResolucion (float): Días promedio transcurridos para resolver un expediente.
        pendientesUltimaSemana (int): Reportes pendientes registrados en los últimos 7 días.
        porcentajeEnProceso (float): Porcentaje de reportes que se encuentran en seguimiento.
        porcentajePendientes (float): Porcentaje de reportes que aún no inician seguimiento.
    """
    promedioResolucion: float = Field(
        ...,
        description="Promedio de días requeridos para concluir satisfactoriamente un caso.",
        examples=[12.4]
    )
    pendientesUltimaSemana: int = Field(
        ...,
        description="Cantidad de casos sin resolver registrados durante la última semana.",
        examples=[8]
    )
    porcentajeEnProceso: float = Field(
        ...,
        description="Porcentaje del total de reportes que se encuentran actualmente en seguimiento.",
        examples=[41.2]
    )
    porcentajePendientes: float = Field(
        ...,
        description="Porcentaje del total de reportes que están pendientes de asignación o revisión.",
        examples=[23.8]
    )

class CantidadReportes(BaseModel):
    """Resumen cuantitativo global de la distribución de reportes por categorías de atención.

    Attributes:
        total (int): Volumen total histórico de reportes registrados.
        completados (int): Total de reportes con estatus concluido.
        en_proceso (int): Total de reportes en revisión o seguimiento.
        pendientes (int): Total de reportes en estatus inicial registrado.
    """
    total: int = Field(
        ...,
        description="Volumen general histórico de reportes en la plataforma.",
        examples=[150]
    )
    completados: int = Field(
        ...,
        description="Cantidad de reportes que concluyeron favorablemente.",
        examples=[60]
    )
    en_proceso: int = Field(
        ...,
        description="Cantidad de reportes que se encuentran en atención activa o revisión.",
        examples=[55]
    )
    pendientes: int = Field(
        ...,
        description="Cantidad de reportes recién registrados en espera de primer contacto.",
        examples=[35]
    )


