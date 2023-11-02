pyinstaller --hidden-import "babel.numbers" --hidden-import "mysql.connector.locales.eng" --hidden-import "mysql.connector.locales.eng.client_error" pajer.py --windowed --noconfirm
mkdir D:\VisualStudio_Projects\Pajer\dist\pajer\sql
mkdir D:\VisualStudio_Projects\Pajer\dist\pajer\img
copy D:\VisualStudio_Projects\Pajer\img\*.* D:\VisualStudio_Projects\Pajer\dist\pajer\img\
copy D:\VisualStudio_Projects\Pajer\sql\*.* D:\VisualStudio_Projects\Pajer\dist\pajer\sql\