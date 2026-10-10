# Tutoría API 🎓

API RESTful robusta construida con **FastAPI**, **SQLModel**, **JWT** y **OAUTH2** para la gestión integral de un area de trabajo grupal. Diseñada para administrar usuarios, controlar el presentismo (asistencias) y coordinar un sistema de tareas colaborativo con filtrado dinámico.

## 🚀 Tecnologías Principales

*   **Framework Web:** FastAPI
*   **ORM & Validación:** SQLModel (basado en SQLAlchemy y Pydantic)
*   **Base de Datos:** MySQL (con soporte para migraciones / esquemas relacionales)
*   **Servidor ASGI:** Uvicorn
*   **Seguridad:** Hashing de contraseñas y validación de roles basada en dependencias (Dependency Injection).

## 🏗️ Arquitectura del Proyecto

El proyecto sigue un patrón de diseño estructurado en capas para separar las responsabilidades, facilitando el mantenimiento y la escalabilidad:

*   **`models/`**: Define los esquemas de bases de datos y los modelos de validación de Pydantic (Create, Read, Update).
*   **`routers/`**: Contiene los controladores y endpoints de la API, manejando las peticiones HTTP y la inyección de dependencias.
*   **`services/`**: Encapsula la lógica de negocio y las operaciones complejas de base de datos, manteniendo los routers limpios.
*   **`core/`**: Configuración central, dependencias globales de base de datos (`SessionDep`) y utilidades de autenticación/seguridad.

## ⚙️ Módulos Implementados

### 1. Gestión de Usuarios y Seguridad
*   Autenticación y autorización mediante JWT con algoritmo HS256.
*   Control de acceso basado en roles (`ADMIN`, `SUPER_USER`, usuarios estándar).
*   Mutación segura de datos: Intercepción y hasheo automático de contraseñas en operaciones `PATCH` mediante Argon2.
*   Prevención de escalada de privilegios (restricción de modificación de roles).

### 2. Control de Asistencias
*   Registro y seguimiento del presentismo del equipo de trabajo.
*   Endpoints dedicados para el conteo de inasistencias.
*   Integración directa de métricas en el perfil del usuario (`/me`).

### 3. Sistema de Tareas (Gestión Colaborativa)
*   CRUD completo para la asignación y seguimiento de tareas institucionales.
*   Relación de base de datos (Claves Foráneas) entre `UserDB` y `Tarea`.
*   **Filtrado Dinámico:** Búsqueda y filtrado de tareas por estado, fecha y coincidencias parciales de nombre mediante queries construidas condicionalmente (`icontains`).
*   Paginación nativa (`skip`, `limit`) delegada a la capa de servicios.

## 💻 Instalación y Ejecución Local

Este proyecto utiliza `uv` como gestor de paquetes y dependencias ultra-rápido, configurado mediante `pyproject.toml`.

1. Clonar el repositorio:
   git clone [https://github.com/Cristian1335/Tutores-API.git](https://github.com/Cristian1335/Tutores-API.git)
   cd tutoria-api

    1.1. Levantar la Base de Datos
        Asegúrate de tener [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado y ejecutándose.
        En la raíz del proyecto, inicializa la base de datos con el comando:
        docker compose up -d
    1.2. 1.2. Crea un archivo `.env` en la raíz del proyecto para configurar tus credenciales. La API requiere las siguientes variables para funcionar:
   
        DB_NAME = nombre_de_la_bd
        DB_PASSWORD = password_de_tu_bd
        DB_USER = tu_usuario
        DB_HOST = host
        DB_PORT = puerto
        SECRET_KEY="tu_clave_secreta_para_jwt"
        ALGORITHM="algoritmo usado para jwt"

3. Instalar las dependencias:
    # uv creará automáticamente el entorno virtual (.venv) e instalará todo lo declarado en pyproject.toml
    uv sync

4. Activar entorno virtual: 
    # En Windows:
        .venv/Scripts/activate
    # En Linux/Mac:
        source .venv/bin/activate

5. Ejecutar el servidor de desarrollo:
    uvicorn main:app --reload

6. Acceder a la documentación interactiva provista por FastAPI en: http://localhost:8000/docs.

**Próximos Pasos (Roadmap)**

  [ ] Módulo de Estadísticas: Creación de endpoints de agregación de datos para la generación de gráficos de carga de trabajo.
  
  [ ] Integración con IA: Implementación de análisis predictivo sobre los picos de consultas y tareas utilizando Modelos de Lenguaje Grandes (LLMs) para la toma de decisiones en la asignación de tutores.
