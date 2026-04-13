# 🧩 S2O API — Smart Restaurant Management Platform

Backend API service built with **FastAPI**, **PostgreSQL**, **RabbitMQ**, and **Redis**. Implements MVC + Clean Architecture for a scalable SaaS restaurant management system.

---

## 📋 Table of Contents
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
  - [Local Development](#local-development)
  - [Docker Compose](#docker-compose)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Database Migrations](#database-migrations)
- [Testing & Quality](#testing--quality)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## Prerequisites

### For Local Development
- **Python 3.10+**
- **PostgreSQL 14+** (running locally or via Docker)
- **RabbitMQ 3+** (optional, for async tasks)
- **Redis** (optional, for caching)
- **pip** (Python package manager)

### For Docker
- **Docker 20.10+**
- **Docker Compose 2.0+**
- **4GB+ RAM** (recommended)

---

## Quick Start

### Local Development

#### 1. Clone & Setup
```bash
git clone <repo-url>
cd s2o-api
```

#### 2. Create Virtual Environment
```bash
# Linux / macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

#### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Environment Configuration
Copy and configure environment file:
```bash
cp .env.example .env.local
```

Edit `.env.local`:
```env
DATABASE_URL=postgresql://postgres:123456@localhost:5432/s2o_db
ENV=development
JWT_SECRET_KEY=your_secret_key_here
RABBITMQ_URL=amqp://guest:guest@localhost:5672/
REDIS_URL=redis://localhost:6379
MEDIA_ROOT=./media
PORT=8000
```

#### 5. Start PostgreSQL (if local)
```bash
# Using Docker
docker run --name s2o-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=123456 \
  -e POSTGRES_DB=s2o_db \
  -p 5432:5432 \
  -d postgres:16

# Or use your local PostgreSQL setup
```

#### 6. Run Database Migrations
```bash
alembic upgrade head
```

#### 7. Start Development Server
```bash
# Option A: Direct uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Option B: Using provided script
./run.sh           # Linux/macOS
run.ps1           # Windows
```

Server runs at: **http://localhost:8000**

API Docs: **http://localhost:8000/docs** (Swagger UI)

---

### Docker Compose

#### 1. Clone Repository
```bash
git clone <repo-url>
cd s2o-api
```

#### 2. Configure Environment
```bash
cp .env.docker .env.docker.local
# Edit if needed (defaults work for local)
```

#### 3. Start Services
```bash
# Build & start all services (PostgreSQL, RabbitMQ, API)
docker-compose up -d

# View logs
docker-compose logs -f

# View API logs
docker-compose logs -f api
```

Services will be available at:
- **API:** http://localhost:8001
- **Swagger UI:** http://localhost:8001/docs
- **PostgreSQL:** localhost:5432
- **RabbitMQ Console:** http://localhost:15672 (guest/guest)

#### 4. Stop Services
```bash
docker-compose down

# Remove volumes (database data)
docker-compose down -v
```

---

## Project Structure

```
s2o-api/
├── controllers/              # Route handlers (FastAPI routers)
│   ├── auth_controller.py
│   ├── restaurant_controller.py
│   ├── menu_item_controller.py
│   ├── order_controller.py
│   └── ...
│
├── models/                   # SQLAlchemy ORM models
│   ├── user.py
│   ├── restaurant.py
│   ├── menu_item.py
│   ├── order.py
│   └── ...
│
├── schemas/                  # Pydantic request/response models
│   ├── auth_schema.py
│   ├── restaurant_schema.py
│   ├── order_schema.py
│   └── ...
│
├── utils/                    # Helper utilities
│   ├── security.py          # Password hashing & JWT
│   ├── jwt.py               # Token creation/validation
│   ├── dependencies.py      # FastAPI dependencies
│   ├── permissions.py       # Authorization checks
│   ├── rabbitmq.py          # RabbitMQ integration
│   ├── redis.py             # Redis cache
│   ├── analytics.py         # Business logic
│   └── ...
│
├── db/                       # Database setup
│   ├── database.py          # SQLAlchemy config
│   ├── session.py           # DB session management
│   └── __init__.py
│
├── alembic/                  # Database migrations
│   ├── env.py
│   ├── versions/
│   └── alembic.ini
│
├── tests/                    # Unit & integration tests
│   ├── test_auth.py
│   ├── test_restaurant.py
│   └── ...
│
├── main.py                   # FastAPI app entry point
├── requirements.txt          # Python dependencies (local)
├── requirements.docker.txt   # Docker dependencies
├── docker-compose.yml        # Docker Compose config
├── Dockerfile                # Docker image build
├── entrypoint.sh             # Docker startup script
├── .env.example              # Example env variables
├── .env.docker               # Docker env defaults
├── pyproject.toml            # Ruff linter config
└── README.md                 # This file
```

---

## Configuration

### Environment Variables

**Local Development** (`.env.local`):
```env
# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/s2o_db

# Application
ENV=development
PORT=8000
BASE_URL=http://localhost:8000

# Security
JWT_SECRET_KEY=dev_secret_key_change_in_production

# Message Queue
RABBITMQ_URL=amqp://guest:guest@localhost:5672/

# Cache
REDIS_URL=redis://localhost:6379

# File Storage
MEDIA_ROOT=./media

# Firebase (optional)
FIREBASE_CREDENTIALS_PATH=./secrets/firebase-key.json
```

**Docker** (`.env.docker`):
```env
DATABASE_URL=postgresql://postgres:123456@postgres:5432/s2o_db
ENV=production
JWT_SECRET_KEY=change_me_in_production
RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/
REDIS_URL=redis://redis:6379
MEDIA_ROOT=/app/media
BASE_URL=http://localhost:8001
```

---

## Database Migrations

### Create New Migration
```bash
# Auto-detect model changes
alembic revision --autogenerate -m "Add user roles table"

# View generated migration in alembic/versions/
```

### Apply Migrations
```bash
# Apply all pending migrations
alembic upgrade head

# Apply specific version
alembic upgrade <revision_id>

# Rollback one migration
alembic downgrade -1

# Rollback to specific version
alembic downgrade <revision_id>
```

### View Migration History
```bash
alembic history
```

---

## Testing & Quality

### Run Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html --cov-report=xml

# Run specific test file
pytest tests/test_auth.py

# Run tests matching pattern
pytest -k "test_register"

# Verbose output
pytest -v
```

### Linting & Code Quality
```bash
# Check code style (Ruff)
ruff check .

# Auto-fix style issues
ruff check . --fix

# Format code
ruff format .
```

### Test Configuration
Use `.env.test.example` for test environment setup.

---

## API Documentation

### Swagger UI
Access interactive API documentation:
```
http://localhost:8000/docs
```

### Key Endpoints

#### Authentication
- `POST /auth/register` — Register new user
- `POST /auth/login` — Login & get JWT token
- `GET /auth/me` — Get current user info

#### Restaurants
- `GET /restaurants` — List restaurants
- `POST /restaurants` — Create restaurant (admin)
- `GET /restaurants/{id}` — Get restaurant details
- `PUT /restaurants/{id}` — Update restaurant

#### Menu
- `GET /menus` — List menu items
- `POST /menus` — Create menu item
- `PUT /menus/{id}` — Update menu item

#### Orders
- `GET /orders` — List orders
- `POST /orders` — Create order
- `PUT /orders/{id}/status` — Update order status

#### More routes available in `/docs`

---

## Troubleshooting

### Local Development Issues

#### Port Already in Use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9     # Linux/macOS
netstat -ano | findstr :8000       # Windows (find PID, then taskill)
```

#### PostgreSQL Connection Failed
```bash
# Check PostgreSQL is running
psql -U postgres -h localhost -d s2o_db

# If Docker container:
docker ps | grep postgres
docker logs s2o-postgres
```

#### Database Migration Error
```bash
# Reset migrations (development only)
alembic stamp base
alembic upgrade head
```

### Docker Issues

#### Container Won't Start
```bash
# View detailed logs
docker-compose logs api
docker-compose logs postgres

# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

#### Network/iptables Error
```bash
# Fix iptables conflict with Docker
sudo update-alternatives --set iptables /usr/sbin/iptables-legacy
sudo systemctl restart docker
docker-compose up -d
```

#### Port Conflicts
```bash
# Change port in docker-compose.yml
# ports:
#   - "8002:8000"  # Use 8002 instead of 8001
```

#### Database Not Initializing
```bash
# Check if init SQL executed
docker exec s2o-postgres psql -U postgres -d s2o_db -c "\dt"

# Manually run init
docker exec s2o-postgres psql -U postgres -d s2o_db < s2o_db_empty.sql
```

---

## Development Workflow

### 1. Create Feature Branch
```bash
git checkout -b feature/new-feature
```

### 2. Make Changes
- Create models in `models/`
- Create schemas in `schemas/`
- Create routes in `controllers/`
- Add business logic in `utils/`
- Write tests in `tests/`

### 3. Test Locally
```bash
pytest --cov=.
ruff check . --fix
```

### 4. Run via Docker (Final Check)
```bash
docker-compose up -d
# Test at http://localhost:8001
```

### 5. Commit & Push
```bash
git add .
git commit -m "feat: add new feature"
git push origin feature/new-feature
```

---

## Performance & Monitoring

### View API Metrics
```
http://localhost:8000/metrics  (Prometheus format)
```

### Check Database Connections
```bash
psql -U postgres -d s2o_db -c "SELECT count(*) FROM pg_stat_activity;"
```

### Monitor RabbitMQ
```
http://localhost:15672  (default: guest/guest)
```

---

## Production Deployment

### Security Checklist
- [ ] Change `JWT_SECRET_KEY` to random string
- [ ] Use strong PostgreSQL password
- [ ] Enable HTTPS (reverse proxy: nginx/Caddy)
- [ ] Restrict CORS origins (remove "*")
- [ ] Set `ENV=production`
- [ ] Use managed PostgreSQL (AWS RDS, Managed Databases)
- [ ] Use managed RabbitMQ service
- [ ] Set up monitoring & logging

### Deploy with Docker
```bash
docker build -t s2o-api:latest .
docker run -d \
  --name s2o-api \
  -e DATABASE_URL=postgresql://... \
  -e JWT_SECRET_KEY=... \
  -p 8000:8000 \
  s2o-api:latest
```

---

## System Architecture

Full architecture, API flows, and database schema:

📖 [Complete Documentation](https://github.com/huytran2005/s2o-docs/blob/master/README.md)

---

## Contributing

1. Fork repository
2. Create feature branch: `git checkout -b feature/xxx`
3. Write tests for changes
4. Run linter: `ruff check . --fix`
5. Commit: `git commit -m "feat: description"`
6. Push & create Pull Request
