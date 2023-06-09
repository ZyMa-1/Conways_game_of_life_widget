# Conways_game_of_life_widget
Custom widget using PySide6 and Python 3.10 version.  
Integratable with Qt Designer.  
Has ConfigManager, which can save properties in a json file and then load them back to widget.  

# Building with Nuitka
Install nuitka in your venv:
```
pip3 install nuitka
```

**Building standalone:**  
</br>
Run following command:
```
nuitka --standalone --follow-imports --quiet --disable-console --plugin-enable=pyside6 --output-filename=conways_game_of_life.exe .\main.py
```
This will create `main.build/` and `main.dist/` directory. Executable file contains in a dist directory.
</br>
**Building one file:**  
</br>
Run following command:
```
nuitka --onefile --follow-imports --quiet --disable-console --plugin-enable=pyside6 --output-filename=conways_game_of_life.exe .\main.py
```
This will create `main.oneilfe-build/` directory. Executable file contains in a project root directory.

# Screenshots  
  
![MainWindow screeshot](/readme_images/1.png)  
  
![Qt Designer screenshot 1](/readme_images/2.png)  
  
![Qt Designer screenshot 1](/readme_images/3.png)

# Thanks to qtforpython-6 documentation:
 1. https://doc.qt.io/qt-6/designer-using-custom-widgets.html
 2. https://doc.qt.io/qtforpython-6/deployment/index.html
