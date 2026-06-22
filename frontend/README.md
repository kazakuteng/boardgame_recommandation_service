# Vue frontend

This folder contains the Vue version of the existing Django template UI.

## Run

From `frontend`:

```bash
npm install
npm run dev
```

Run Django separately from the project root:

```bash
python manage.py runserver 127.0.0.1:8000
```

The Vite dev server proxies `/boardgames`, `/accounts`, and `/community` to Django.
