@echo off
python -m pip install -r requirements.txt
pyinstaller --noconfirm --onefile --windowed --name Kalashnikova_BOQ_Split_FIXED run_app.py
pause
