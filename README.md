# Conways_game_of_life_widget
Custom widget using PySide6 and Python 3.10 version.
Integratable with Qt Designer.  
Has ConfigManager, which can save properties in a json file and then load them to the widget.  

# Building with Nuitka
Install nuitka in your venv:
```
pip3 install nuitka
```

Run following command:
```
nuitka --standalone --plugin-enable=pyside6 .\main.py
```
This will create `main.build/` and `main.dist/` directory.

# Screenshots  
  
![MainWindow screeshot](/readme_images/1.png)  
  
![Qt Designer screenshot 1](/readme_images/2.png)  
  
![Qt Designer screenshot 1](/readme_images/3.png)
