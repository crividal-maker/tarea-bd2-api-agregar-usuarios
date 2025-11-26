Configuración Inicial del Backend

Comencé configurando el entorno del backend utilizando uv sync para instalar todas las dependencias especificadas en pyproject.toml. Decidí trabajar con SQLite en lugar de PostgreSQL por su simplicidad en desarrollo, por lo que modifiqué el archivo .env con la cadena de conexión:

sqlite:///./bd2_library.db

También actualicé app/config.py para usar SQLite por defecto. En este proceso ajusté algunos detalles del código base entregado por el docente, como corregir el nombre de la variable del secreto JWT, que estaba definida como JWT_SECRET_KEY aunque el código esperaba JWT_SECRET. Para afinar estos detalles revisé referencias y soluciones que ayudaron a verificar que la configuración coincidiera con el comportamiento esperado.

Implementación de Controladores y Seguridad

Implementé todos los controladores necesarios para el proyecto. En app/controllers/user.py creé el UserController con operaciones CRUD completas, agregando exclude_from_auth=True al endpoint de creación de usuarios para permitir registros públicos sin autenticación previa. Este punto me llevó a revisar distintas formas de manejar la autorización, lo que ayudó a resolver el problema que impedía crear usuarios desde el frontend.

El controlador de autenticación en app/controllers/auth.py implementa el login verificando contraseñas hasheadas con Argon2 y retornando tokens JWT. Adicionalmente configuré varios DTOs en app/dtos/user.py: UserReadDTO excluye la contraseña en las respuestas, UserCreateDTO excluye campos autogenerados y UserUpdateDTO permite actualizaciones parciales. Los repositorios utilizan SQLAlchemySyncRepository con un método especial add_with_hashed_password que hashea automáticamente las contraseñas antes de guardarlas.

Otro desafío fue habilitar CORS en el backend, ya que las peticiones desde el frontend (localhost:5173) eran bloqueadas por el navegador. Para solucionarlo agregué CORSConfig en app/__init__.py, permitiendo explícitamente peticiones desde el origen del frontend con los métodos y headers necesarios.

Base de Datos y Pruebas

Ejecuté las migraciones con uv run alembic upgrade head, creando la base de datos SQLite con todas las tablas necesarias, incluyendo los campos de auditoría automática. Probé la funcionalidad creando usuarios de prueba usando curl: primero los usuarios “test” y “test2”, y luego usuarios con nombres
