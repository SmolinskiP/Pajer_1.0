python C:\Users\szatan0802\AppData\Roaming\Python\Python311\Scripts\vba_extract.py D:\VisualStudio_Projects\Pajer\macro.xlsm
pyinstaller --hidden-import "babel.numbers" --hidden-import "mysql.connector.locales.eng" --hidden-import "mysql.connector.locales.eng.client_error" pajer.py --windowed --noconfirm
mkdir D:\VisualStudio_Projects\Pajer\dist\pajer\sql
mkdir D:\VisualStudio_Projects\Pajer\dist\pajer\img
mkdir D:\VisualStudio_Projects\Pajer\dist\pajer\update_db
copy D:\VisualStudio_Projects\Pajer\img\*.* D:\VisualStudio_Projects\Pajer\dist\pajer\img\
copy D:\VisualStudio_Projects\Pajer\sql\*.* D:\VisualStudio_Projects\Pajer\dist\pajer\sql\
copy D:\VisualStudio_Projects\Pajer\vbaProject.bin D:\VisualStudio_Projects\Pajer\dist\pajer\
copy D:\VisualStudio_Projects\Pajer\exe\dist\update_db.exe D:\VisualStudio_Projects\Pajer\dist\pajer\
Xcopy D:\VisualStudio_Projects\Pajer\exe\dist D:\VisualStudio_Projects\Pajer\dist\pajer\update_db /E /H /C /I
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" "C:\Users\szatan0802\OneDrive - PDAserwis\Desktop\PajerScript_Actual.iss"