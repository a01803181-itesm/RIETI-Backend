# RIETI Backend API

Backend RESTful para la plataforma **RIETI** (*Red para la Identificación y Erradicación del Trabajo Infantil*), diseñado para recopilar, canalizar y analizar reportes ciudadanos de presuntas situaciones de trabajo infantil, facilitando la intervención de autoridades competentes mediante dashboards analíticos y geolocalización.

Construido con **FastAPI**, **Python 3.13**, **Pydantic v2**, **MySQL (asyncmy)**, y asegurado con **AWS Cognito**.

---

## Arquitectura Modularizada

El proyecto sigue una arquitectura modular en capas que separa de manera estricta las responsabilidades de configuración, modelos de datos, persistencia y enrutamiento HTTP:

```
backend/
├── app/
│   ├── api/                 # Capa de presentación y enrutamiento HTTP
│   │   ├── router.py        # Enrutador principal raíz (prefijo /v1)
│   │   └── v1/
│   │       ├── api.py       # Registro y montaje de endpoints v1
│   │       └── endpoints/   # Controladores por entidad (admin, alimentador, reporte, etc.)
│   ├── core/                # Configuraciones transversales del sistema
│   │   ├── config.py        # Carga de variables de entorno mediante Pydantic BaseSettings
│   │   ├── db_connection.py # Dependencia get_db para inyección en endpoints
│   │   ├── mysql.py         # Administrador del pool asíncrono de conexiones (asyncmy)
│   │   ├── security.py      # Autenticación JWT y validación criptográfica con AWS Cognito
│   │   └── logs.py          # Configuración de bitácoras con colores ANSI y nivel SUCCESS
│   ├── crud/                # Capa de persistencia y lógica SQL asíncrona
│   │   ├── admin.py         # Consultas e inserciones para Administradores
│   │   ├── alimentador.py   # Consultas e inserciones para Autoridades/Alimentadores
│   │   ├── usuario.py       # Consultas y registro de Usuarios ciudadanos
│   │   └── reporte.py       # Operaciones de reportes, geolocalización y métricas KPI
│   ├── schemas/             # Modelos de dominio, DTOs y validación Pydantic
│   │   ├── enums.py         # Enumeraciones (Provider, Status, RangoEdad, TipoTrabajo)
│   │   ├── admin.py         # Esquema de Administrador
│   │   ├── alimentador.py   # Esquema de Alimentador/Autoridad
│   │   ├── usuario.py       # Esquemas de Usuario y verificación de correo
│   │   ├── reporte.py       # Esquemas de Reporte, coordenadas y agregaciones métricas
│   │   ├── expediente.py    # Esquema de Expediente administrativo
│   │   ├── evidencia.py     # Esquema de Evidencias multimedia
│   │   └── admin_reporte.py # Esquema de bitácora admin-reporte
│   ├── .env.example         # Plantilla local de variables de entorno
│   └── main.py              # Instancia de FastAPI, middleware CORS, lifespan y handler Mangum
├── db_architecture/         # Scripts DDL y esquemas SQL relacionales
├── .gitignore               # Exclusión de archivos sensibles (.env) y temporales
├── requirements.txt         # Lista exhaustiva de dependencias del proyecto
└── README.md                # Documentación técnica integral
```

### Responsabilidades por Capa:

1. **`/app/api` (Rutas & OpenAPI):** Expone las interfaces REST. Cada endpoint está decorado con metadatos OpenAPI (`summary`, `description`, `responses`), garantizando contratos de API autodescriptivos en Swagger UI.
2. **`/app/core` (Configuración & Seguridad):** Administra la inicialización segura del pool de base de datos (`MySQLManager`), la validación de tokens Bearer JWT contra los endpoints JWKS de AWS Cognito y la parametrización de variables de entorno.
3. **`/app/crud` (Acceso a Datos):** Encapsula todas las sentencias SQL parametrizadas para mitigar riesgos de Inyección SQL (SQLi), ejecutando transacciones asíncronas de alto rendimiento con `asyncmy`.
4. **`/app/schemas` (Validación & Contratos):** Define modelos que heredan de `BaseModel` tipados estrictamente y documentados con `Field(..., description="...")` para enriquecer la interfaz interactiva.

---

## Requisitos Previos

* **Python:** 3.10 o superior (recomendado: Python 3.13).
* **Motor de Base de Datos:** MySQL Server 8.0+ o MariaDB 10.5+ (local o en la nube mediante AWS RDS).
* **Administrador de paquetes:** `pip` actualizado.
* **Control de versiones:** Git.

---

## Guía de Instalación Local con Entorno Virtual (`venv`)

Para garantizar el aislamiento de dependencias y evitar conflictos entre paquetes globales del sistema, el proyecto debe ejecutarse dentro de un entorno virtual Python (`venv`).

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd backend
```

### 2. Crear el entorno virtual

En la raíz del proyecto (`backend`), ejecuta:

```bash
python -m venv .venv
```

### 3. Activar el entorno virtual

* **En Windows (PowerShell):**

  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```

  > [!TIP]
  > Si PowerShell bloquea la ejecución de scripts por directivas de seguridad, habilita temporalmente la sesión ejecutando:
  >
  > ```powershell
  > Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
  > ```
  >
* **En Windows (Símbolo del sistema / CMD):**

  ```cmd
  .\.venv\Scripts\activate.bat
  ```
* **En macOS / Linux (Bash o Zsh):**

  ```bash
  source .venv/bin/activate
  ```

Al activarse correctamente, verás el prefijo `(.venv)` en la línea de comandos de tu terminal.

### 4. Actualizar pip e instalar dependencias

Con el entorno virtual activado, instala todas las librerías necesarias:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## Configuración de Variables de Entorno y Seguridad

El sistema utiliza **Pydantic Settings** y **python-dotenv** para cargar configuraciones sensibles sin exponerlas en el código fuente.

### 1. Generar tu archivo `.env` y Parámetros de Configuración

Crea el archivo `app/.env` e inyecta los valores correspondientes a tu infraestructura:

| Variable                  | Tipo          | Descripción                              | Ejemplo                       |
| :------------------------ | :------------ | :---------------------------------------- | :---------------------------- |
| `MYSQL_DB_HOST`         | `str`       | Host o dirección IP del servidor MySQL   | `localhost`                 |
| `MYSQL_DB_PORT`         | `str`       | Puerto del servicio MySQL                 | `3306`                      |
| `MYSQL_DB_NAME`         | `str`       | Nombre de la base de datos relacional     | `rieti_db`                  |
| `MYSQL_DB_USER`         | `str`       | Usuario con permisos de BD                | `rieti_user`                |
| `MYSQL_DB_PASSWORD`     | `str`       | Contraseña del usuario de BD             | `secreto_db_123`            |
| `AWS_COGNITO_REGION`    | `str`       | Región AWS del User Pool                 | `us-east-1`                 |
| `COGNITO_USER_POOL_ID`  | `str`       | ID del User Pool de AWS Cognito           | `us-east-1_abcdef123`       |
| `ANDROID_APP_CLIENT_ID` | `str`       | Client ID de la app móvil en Cognito     | `6s8d7f6s8d7f6s8d7f6s8d7f`  |

### Prácticas de Seguridad:

> [!IMPORTANT]
> - **Autenticación JWT:** Las rutas protegidas verifican criptográficamente el token con las llaves públicas RSA de Cognito (`RS256`) y cotejan emisor y audiencia.
> - **Consultas SQL Parametrizadas:** Toda interacción con la base de datos a través de `asyncmy` utiliza marcadores de posición `%s` para prevenir vulnerabilidades de inyección SQL.

---

## Ejecución del Servidor en Desarrollo

Para iniciar el servidor local con recarga en caliente (*hot reload*):

```bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Si deseas especificar la ruta del archivo `.env` al ejecutar:

```powershell
$env:ENV_FILE="app/.env"; uvicorn app.main:app --reload
```

---

## Documentación Interactiva de la API

Una vez iniciado el servidor, accede a la documentación viva autogenerada por OpenAPI:

* **Swagger UI (Pruebas interactivas):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **ReDoc (Documentación técnica limpia):** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
* **Esquema OpenAPI JSON:** [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)

---

## Catálogo de Rutas Principales de la API (v1)

Todos los endpoints se encuentran organizados bajo el prefijo `/v1`:

### 1. Verificación de Salud (Health Check)

| Método | Ruta          | Resumen / Descripción                     | Respuestas HTTP           |
| :------ | :------------ | :----------------------------------------- | :------------------------ |
| `GET` | `/v1/check` | Comprueba el estado operativo del backend. | `200` OK, `500` Error |

### 2. Administradores (`/v1/admins`)

| Método  | Ruta                         | Resumen / Descripción                                      | Respuestas HTTP                          |
| :------- | :--------------------------- | :---------------------------------------------------------- | :--------------------------------------- |
| `GET`  | `/v1/admins/{admin_email}` | Obtiene los datos de perfil de un administrador por correo. | `200` Admin, `404`, `422`, `500` |
| `GET`  | `/v1/admins`               | Lista todos los administradores registrados.                | `200` list[Admin], `500`             |
| `POST` | `/v1/admins`               | Registra a un nuevo administrador en el sistema.            | `201` Admin, `400`, `422`, `500` |

### 3. Alimentadores / Autoridades (`/v1/alimentadores`)

| Método  | Ruta                               | Resumen / Descripción                                             | Respuestas HTTP                                |
| :------- | :--------------------------------- | :----------------------------------------------------------------- | :--------------------------------------------- |
| `GET`  | `/v1/alimentadores/{alim_email}` | Obtiene los datos de una autoridad por su correo institucional.    | `200` Alimentador, `404`, `422`, `500` |
| `GET`  | `/v1/alimentadores`              | Lista todas las autoridades y alimentadores registrados.           | `200` list[Alimentador], `500`             |
| `POST` | `/v1/alimentadores`              | Registra un nuevo funcionario o autoridad asignado a un municipio. | `201` Alimentador, `400`, `422`, `500` |

### 4. Usuarios Ciudadanos (`/v1/usuarios`)

| Método  | Ruta                                 | Resumen / Descripción                                            | Respuestas HTTP                            |
| :------- | :----------------------------------- | :---------------------------------------------------------------- | :----------------------------------------- |
| `GET`  | `/v1/usuarios/{user_email}`        | Obtiene información del perfil de un usuario ciudadano.          | `200` Usuario, `404`, `422`, `500` |
| `GET`  | `/v1/usuarios`                     | Lista todos los usuarios ciudadanos registrados.                  | `200` list[Usuario], `500`             |
| `POST` | `/v1/usuarios`                     | Registra a un nuevo ciudadano con su proveedor de autenticación. | `201` Usuario, `400`, `422`, `500` |
| `GET`  | `/v1/usuarios/check-email/{email}` | Comprueba si un correo ya existe y devuelve su proveedor.         | `200` CheckEmail, `422`, `500`       |

### 5. Reportes de Trabajo Infantil y Métricas (`/v1/reportes`)

| Método  | Ruta                                                   | Resumen / Descripción                                                 | Respuestas HTTP                            |
| :------- | :----------------------------------------------------- | :--------------------------------------------------------------------- | :----------------------------------------- |
| `GET`  | `/v1/reportes`                                       | Lista todos los reportes de presunto trabajo infantil.                 | `200` list[Reporte], `500`             |
| `POST` | `/v1/reportes`                                       | Registra un nuevo reporte con geolocalización y datos de menor.       | `201` Reporte, `422`, `500`          |
| `GET`  | `/v1/reportes/{folio}`                               | Consulta el detalle completo de un reporte por su folio único.        | `200` Reporte, `404`, `422`, `500` |
| `GET`  | `/v1/reportes/by-user/{user_email}`                  | Obtiene los reportes generados por un ciudadano específico.           | `200` list[Reporte], `422`, `500`    |
| `GET`  | `/v1/reportes/mapa-calor`                            | Coordenadas (`lat`, `lng`) para capas y mapas de calor.            | `200` list[CoordenadaReporte], `500`   |
| `GET`  | `/v1/reportes/estadisticas/fecha`                    | Conteo de incidentes agrupados por mes.                                | `200` list[CategoriaTotal], `500`      |
| `GET`  | `/v1/reportes/estadisticas/municipio`                | Cantidad de reportes desglosados por municipio.                        | `200` list[CategoriaTotal], `500`      |
| `GET`  | `/v1/reportes/estadisticas/por-rango-hora`           | Conteo de reportes según la hora del día (0-23 hrs).                 | `200` list[CategoriaTotal], `500`      |
| `GET`  | `/v1/reportes/estadisticas/por-autoridad`            | Total de reportes atendidos por cada autoridad responsable.            | `200` list[CategoriaTotal], `500`      |
| `GET`  | `/v1/reportes/estadisticas/por-estatus`              | Distribución de casos según su estado actual de expediente.          | `200` list[CategoriaTotal], `500`      |
| `GET`  | `/v1/reportes/estadisticas/por-estatus/{estatus}`    | Conteo directo de reportes para un estatus específico.                | `200` int, `404`, `422`, `500`     |
| `GET`  | `/v1/reportes/estadisticas/promedio-resolucion`      | Días promedio para la conclusión formal de casos resueltos.          | `200` Data, `500`                      |
| `GET`  | `/v1/reportes/estadisticas/pendientes-ultima-semana` | Cantidad de casos pendientes ingresados en los últimos 7 días.       | `200` DataInt, `500`                   |
| `GET`  | `/v1/reportes/pendientes`                            | Porcentaje de reportes que aún no inician seguimiento.                | `200` Data, `500`                      |
| `GET`  | `/v1/reportes/en-proceso`                            | Porcentaje de reportes en fase activa de seguimiento.                  | `200` Data, `500`                      |
| `GET`  | `/v1/reportes/por-estatus/cantidad`                  | Métricas consolidadas (totales, completados, en proceso, pendientes). | `200` CantidadReportes, `500`          |

---

## Compatibilidad Serverless (AWS Lambda)

La aplicación integra **Mangum** como puente ASGI en `app/main.py`:

```python
from mangum import Mangum
handler: Mangum = Mangum(app=app)
```

Esto permite empaquetar el backend en una función **AWS Lambda** expuesta a través de **AWS API Gateway** sin modificaciones adicionales en el código fuente.