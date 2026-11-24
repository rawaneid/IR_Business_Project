
@echo off
cd /d "D:\Uni year 3\IR\IR_Business_Project"

call "C:\myanaconda\Scripts\activate.bat" ir_project

python -m streamlit run app.py

pause
