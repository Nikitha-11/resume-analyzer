@echo off
echo Setting up Resume Analyzer Project...

echo.
echo Installing Backend Dependencies...
cd backend
pip install -r requirements.txt
python -m spacy download en_core_web_sm

echo.
echo Installing Frontend Dependencies...
cd ..\frontend
npm install

echo.
echo Setup Complete!
echo.
echo To run the application:
echo 1. Backend: cd backend && python app.py
echo 2. Frontend: cd frontend && npm start
echo.
pause