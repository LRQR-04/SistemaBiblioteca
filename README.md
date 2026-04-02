# Sistema de Gestión de Biblioteca

Sistema web desarrollado para la administración de una biblioteca, permitiendo gestionar el catálogo de libros, usuarios y préstamos de manera eficiente, segura y modular.

Este proyecto fue desarrollado bajo un enfoque de buenas prácticas de ingeniería de software, incluyendo estándares de codificación, pruebas unitarias, manejo de errores y documentación técnica.

---

## Características principales

- Gestión de libros (registro, búsqueda, actualización de estado)
- Administración de usuarios (admins, estudiantes y profesores)
- Control de préstamos y devoluciones
- Sistema de autenticación y control de roles
- Manejo robusto de errores con excepciones personalizadas
- Pruebas unitarias
- Sistema de logging de errores

---

## Tecnologías utilizadas

### Backend

- Python 3.11+
- SQLite (con posibilidad de migración a PostgreSQL)
- FastAPI (arquitectura API REST)
- SQLAlchemy (ORM)
- Pytest + Coverage (testing)

### Frontend

- Vue.js 3
- Vite
- Axios
- Pinia (gestión de estado)

---

## Estructura del proyecto

```bash
biblioteca-system/
│
├── backend/
│   ├── app/
│   │   ├── core/          # Configuración, seguridad y BD
│   │   ├── models/        # Modelos ORM
│   │   ├── schemas/       # Esquemas (validación)
│   │   ├── services/      # Lógica de negocio
│   │   ├── routes/        # Endpoints API
│   │   ├── middleware/    # Autenticación y roles
│   │   ├── exceptions/    # Excepciones personalizadas
│   │   └── utils/         # Logger
│   │
│   ├── logs/              # Archivo de errores
│   ├── tests/             # Pruebas unitarias
│
├── frontend/
│   ├── components/        # Componentes reutilizables
│   ├── views/             # Vistas principales
│   ├── layouts/           # Layouts
│   ├── router/            # Rutas
│   ├── stores/            # Estado global
│   └── services/          # Comunicación API
```

---

## Instalación y ejecución

### 1. Clonar repositorio

```bash
git clone https://github.com/LRQR-04/SistemaBiblioteca.git
cd biblioteca-system
```

### 2. Backend

```bash
cd backend
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

#### Variables de entorno (.env)

```
DATABASE_URL=sqlite:///./app/data/biblioteca.bd
SECRET_KEY=tu_clave_secreta
ALGORITMO=HS256
EXPIRACION_TOKEN=120
```

#### Ejecutar servidor

```bash
cd backend
python run.py
```

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

#### Variables de entorno (.env)

```
VITE_API_URL=direccion_servidor_backend
```

---

## Arquitectura del sistema

El sistema sigue una arquitectura modular basada en capas:

- **Routes** → Exponen endpoints REST
- **Services** → Contienen la lógica de negocio
- **Models** → Representan la base de datos
- **Schemas** → Validación de datos
- **Core** → Configuración general

📌 Diagrama de arquitectura:

![Arquitectura](./assets/docs/images/arquitectura.png)

---

## Base de datos

El sistema utiliza un modelo relacional con las siguientes entidades:

- **Libros**
- **Usuarios**
- **Préstamos**

📌 Diagrama Entidad-Relación:

![Diagrama ER](./docs/images/diagrama-er.png)

---

## Lógica de negocio (Préstamos)

El sistema implementa reglas críticas:

- ❌ No se permite préstamo si el usuario está suspendido
- ❌ No se permite préstamo sin stock disponible
- ✅ Al prestar → disminuye stock
- ✅ Al devolver → aumenta stock

---

## Pruebas

Se implementaron pruebas unitarias usando Pytest para validar:

- Registro de libros sin duplicidad de ISBN
- Validación de formato de email
- Lógica de préstamos y devoluciones

Ejecutar pruebas:

```bash
pytest
```

---

## Manejo de errores

Se implementaron excepciones personalizadas:

- `LibroNoEncontradoError`
- `UsuarioSuspendidoError`
- `SinStockError`

Además, se registra información en:

```
backend/logs/errors.log
```

---

## Estándares de desarrollo

- PEP 8 (estilo de código)
- Type Hints obligatorios
- Docstrings (formato Google)
- Arquitectura modular
- Separación de responsabilidades

---

## Manual de uso

1. Iniciar el backend
2. Ejecutar el frontend
3. Acceder desde el navegador
4. Iniciar sesión o registrarse
5. Gestionar libros, usuarios y préstamos desde el dashboard

---

## Conclusiones

El desarrollo de este sistema permitió aplicar de forma integral:

- Diseño de arquitectura modular
- Implementación de lógica de negocio robusta
- Validación mediante pruebas unitarias
- Manejo adecuado de errores
- Documentación técnica clara

Estas prácticas son fundamentales para construir sistemas escalables, mantenibles y seguros.

---

## Autor

- LRQR-04
- GitHub: https://github.com/LRQR-04

---
