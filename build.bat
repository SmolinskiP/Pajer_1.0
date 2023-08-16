pyinstaller --hidden-import "babel.numbers" pajer.py --windowed --noconfirm
mkdir D:\VisualStudio_Projects\Pajer\dist\pajer\sql
mkdir D:\VisualStudio_Projects\Pajer\dist\pajer\img
copy D:\VisualStudio_Projects\Pajer\img\*.* D:\VisualStudio_Projects\Pajer\dist\pajer\img\
copy D:\VisualStudio_Projects\Pajer\sql\*.* D:\VisualStudio_Projects\Pajer\dist\pajer\sql\