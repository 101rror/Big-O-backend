## Big-O Django Backend

### Railway deployment checklist

1. Push this repository to GitHub.
2. In Railway, create a new project and connect the GitHub repo.
3. Add these environment variables in Railway:
   - `SECRET_KEY=<strong-random-secret>`
   - `DEBUG=False`
   - `ALLOWED_HOSTS=your-app-name.up.railway.app`
   - `CSRF_TRUSTED_ORIGINS=https://your-app-name.up.railway.app`
   - `DATABASE_URL=<Railway PostgreSQL URL>`
4. Use this start command:
   - `gunicorn api.wsgi:application --bind 0.0.0.0:$PORT`
5. Railway will install dependencies from `requirements.txt`, run migrations, and start the app.

### Local development

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
