REM Points to current dir.
set cur_dir=%cd%

REM Points to parent dir.
for %%B in (%cur_dir%.) do set root_dir=%%~dpB

REM set PATH=%PATH%;%root_dir%;%cur_dir%
set PYTHONPATH=%PYTHON_PATH%;%root_dir%;%cur_dir%

python %cur_dir%\ui_example.py

pause