@echo off
rmdir dist /s /q
rmdir .\build /s /q
cd src
python setup.py install
python setup.py py2exe
rmdir build /s /q
cd ..
copy license.txt .\dist