@echo off
cmd /k "start chrome http://localhost:8000 & cd /d %CD% && .\venv\Scripts\activate & cd /d  %CD% & pip install -r requirements.txt && python manage.py runserver"

