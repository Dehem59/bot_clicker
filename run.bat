@echo off
cmd /k "cd /d %CD% && .\venv\Scripts\activate & cd /d  %CD% & pip install -r requirements.txt && python manage.py runserver && start firefox http://127.0.0.1:8000"
