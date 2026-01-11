# CMS Backend - Educational Content Management System

A Django REST Framework-based CMS for managing educational programs, terms, and lessons with automated publishing workflow and public catalog API.

## Features

- ✅ **Hierarchical Content Management** - Program → Term → Lesson structure
- ✅ **Scheduled Publishing** - Schedule lessons for future publication with automatic publishing worker
- ✅ **Public Catalog API** - Read-only REST API for published content
- ✅ **Admin Interface** - Django admin for content management
- ✅ **Background Worker** - Automatic lesson publishing based on schedule
- ✅ **Docker Support** - Local development with Docker Compose

## Tech Stack

- **Backend**: Django 5.2+, Django REST Framework
- **Database**: SQLite (development), PostgreSQL (production)
- **Task Scheduling**: Django Management Command (can be run via cron/systemd)
- **Containerization**: Docker & Docker Compose

## Quick Start

### Prerequisites
- Python 3.10+
- pip & virtualenv
- (Optional) Docker & Docker Compose

### Local Development Setup

#### 1. Using Python Virtual Environment

```bash
# Clone repository
git clone https://github.com/yourusername/cms-backend.git
cd cms-backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.\.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

Visit http://127.0.0.1:8000/admin/ to access the admin panel.

#### 2. Using Docker Compose

```bash
# Clone repository
git clone https://github.com/yourusername/cms-backend.git
cd cms-backend

# Start services
docker-compose up --build

# In another terminal, run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

Visit http://127.0.0.1:8000/admin/

## API Endpoints

### Catalog API (Read-only, published content only)

```
GET  /catalog/programs/              # List all programs with published lessons
GET  /catalog/programs/<uuid>/        # Get program details
GET  /catalog/lessons/<uuid>/         # Get lesson details
```

**Query Parameters:**
- `language` - Filter by language (e.g., `?language=en`)
- `topic` - Filter by topic name (e.g., `?topic=mathematics`)
- `limit` - Pagination limit (default: 10)
- `offset` - Pagination offset (default: 0)

**Example:**
```bash
curl http://127.0.0.1:8000/catalog/programs/?language=en&limit=5
```

### Admin API (Full CRUD)

```
GET    /api/programs/                 # List programs
POST   /api/programs/                 # Create program
GET    /api/programs/<id>/            # Get program
PUT    /api/programs/<id>/            # Update program
DELETE /api/programs/<id>/            # Delete program

GET    /api/terms/                    # List terms
POST   /api/terms/                    # Create term
GET    /api/lessons/                  # List lessons
POST   /api/lessons/                  # Create lesson
```

## Publishing Workflow

### 1. Create Content
- Login to admin: http://127.0.0.1:8000/admin/
- Create Program → Term → Lesson
- Set lesson `status='draft'`

### 2. Schedule Publishing
- Edit lesson in admin
- Set `status='scheduled'`
- Set `publish_at` timestamp (when it should go live)

### 3. Automatic Publishing
- Worker runs every 60 seconds:
  ```bash
  python manage.py publish_scheduled
  ```
- Publishes all lessons where `publish_at <= current_time`
- Updates lesson `status='published'` and sets `published_at`
- Parent program automatically published if needed

### 4. Appears in Catalog
- Published lessons automatically appear in:
  ```
  GET /catalog/programs/
  ```

## Project Structure

```
cms_backend/
├── cms_backend/              # Django project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── core/                     # Main app (models, views, serializers)
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── catalog_views.py      # Public catalog API
│   ├── admin.py
│   └── migrations/
├── worker/                   # Background worker app
│   ├── management/
│   │   └── commands/
│   │       └── publish_scheduled.py
│   └── migrations/
├── manage.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

## Database Models

### Program
- `id` (UUID)
- `title` (CharField)
- `description` (TextField)
- `status` ('draft', 'published', 'archived')
- `language_primary` (CharField)
- `languages_available` (JSONField)
- `published_at` (DateTimeField)

### Term
- `id` (UUID)
- `program` (ForeignKey → Program)
- `term_number` (IntegerField)
- `title` (CharField)

### Lesson
- `id` (UUID)
- `term` (ForeignKey → Term)
- `lesson_number` (IntegerField)
- `title` (CharField)
- `content_type` ('video', 'article')
- `status` ('draft', 'scheduled', 'published', 'archived')
- `publish_at` (DateTimeField)
- `published_at` (DateTimeField)
- `content_language_primary` (CharField)
- `content_languages_available` (JSONField)
- `content_urls_by_language` (JSONField)
- `is_paid` (BooleanField)

### Topic
- `id` (UUID)
- `name` (CharField)
- `programs` (ManyToManyField → Program)

## Admin Credentials

After running `python manage.py createsuperuser`, use your created credentials to access:
- **Admin Panel**: http://127.0.0.1:8000/admin/

## Worker Setup for Production

### Running the Worker

```bash
# One-time execution
python manage.py publish_scheduled

# Continuous loop (every 60 seconds)
while true; do python manage.py publish_scheduled; sleep 60; done
```

### Systemd Service (Linux)

Create `/etc/systemd/system/cms-worker.service`:

```ini
[Unit]
Description=CMS Publishing Worker
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/cms_backend
ExecStart=/opt/cms_backend/.venv/bin/python manage.py publish_scheduled
Restart=always
RestartSec=60

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable cms-worker
sudo systemctl start cms-worker
```

### Cron Job

```bash
*/1 * * * * cd /path/to/cms_backend && /path/to/.venv/bin/python manage.py publish_scheduled
```

## Testing

### 1. Create a Program

```bash
curl -X POST http://127.0.0.1:8000/api/programs/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Python 101",
    "description": "Learn Python basics",
    "status": "published",
    "language_primary": "en"
  }'
```

### 2. Create a Term

```bash
curl -X POST http://127.0.0.1:8000/api/terms/ \
  -H "Content-Type: application/json" \
  -d '{
    "program": "<program_uuid>",
    "term_number": 1,
    "title": "Basics"
  }'
```

### 3. Create a Lesson

```bash
curl -X POST http://127.0.0.1:8000/api/lessons/ \
  -H "Content-Type: application/json" \
  -d '{
    "term": "<term_uuid>",
    "lesson_number": 1,
    "title": "Introduction",
    "content_type": "video",
    "status": "published",
    "content_language_primary": "en"
  }'
```

### 4. View in Catalog API

```bash
curl http://127.0.0.1:8000/catalog/programs/
```

## Deployment

### Docker

```bash
# Build image
docker build -t cms-backend .

# Run container
docker run -p 8000:8000 \
  -e DEBUG=False \
  -e SECRET_KEY=your-secret-key \
  cms-backend
```

### Deployment Platforms

- **Railway**: Connect GitHub repo, set environment variables, deploy
- **Render**: Same as Railway
- **Heroku**: Add `Procfile` with `web: gunicorn cms_backend.wsgi`
- **AWS/DigitalOcean**: Use Docker image with systemd worker

## Environment Variables

Create a `.env` file based on `.env.example`:

```env
SECRET_KEY=your-production-secret-key
DEBUG=False
DATABASE_URL=postgresql://user:pass@host/dbname
ALLOWED_HOSTS=yourdomain.com,*.railway.app
```

## Troubleshooting

### Database Migration Errors

```bash
# Reset database (development only!)
python manage.py migrate zero
rm db.sqlite3
python manage.py migrate
```

### Static Files Missing

```bash
python manage.py collectstatic --clear --noinput
```

### Port Already in Use

```bash
# Use different port
python manage.py runserver 8001
```

## License

MIT License - See LICENSE file for details

## Contact

For issues or questions, please create a GitHub issue.
