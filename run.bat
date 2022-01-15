@echo off
cmd /k "cd /d %CD% & .\venv\Scripts\activate & cd /d  %CD% & pip install -r requirements.txt & python manage.py runserver & start http://localhost/%~n1%~x1"