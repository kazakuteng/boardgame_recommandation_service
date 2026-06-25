# PythonAnywhere Deployment

## 1. Clone

```bash
git clone https://github.com/olorlo/boardgame_recommandation_service.git
cd boardgame_recommandation_service
```

If you are using the deployment branch:

```bash
git checkout codex/improve-ai-recommendations
```

## 2. Virtualenv

```bash
mkvirtualenv --python=/usr/bin/python3.11 boardgame-venv
pip install -r requirements.txt
```

## 3. Environment

Create `.env` in the project root.

```bash
cp .env.example .env
nano .env
```

Set these values:

```env
SECRET_KEY=replace-this-with-a-long-random-secret-key
DEBUG=False
ALLOWED_HOSTS=yourusername.pythonanywhere.com
CSRF_TRUSTED_ORIGINS=https://yourusername.pythonanywhere.com
GMS_KEY=...
GMS_ENDPOINT=https://gms.ssafy.io/gmsapi/api.openai.com/v1/chat/completions
YOUTUBE_API_KEY=...
BGG_TOKEN=...
```

## 4. Database

```bash
python manage.py migrate
```

Upload `data/game_details.csv` to:

```text
/home/yourusername/boardgame_recommandation_service/data/game_details.csv
```

Then import:

```bash
python manage.py import_game_details data/game_details.csv
```

## 5. Static Files

The Vue build output is committed under `static/vue`, so PythonAnywhere does not need to run `npm run build`.

```bash
python manage.py collectstatic --noinput
```

In the PythonAnywhere Web tab, add static file mappings:

```text
URL: /static/
Directory: /home/yourusername/boardgame_recommandation_service/staticfiles
```

```text
URL: /media/
Directory: /home/yourusername/boardgame_recommandation_service/media
```

## 6. Web App

In the PythonAnywhere Web tab:

1. Add a new web app.
2. Choose manual configuration.
3. Select Python 3.11.
4. Set virtualenv:

```text
/home/yourusername/.virtualenvs/boardgame-venv
```

Edit the WSGI file:

```python
import os
import sys

path = '/home/yourusername/boardgame_recommandation_service'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

Reload the web app.
