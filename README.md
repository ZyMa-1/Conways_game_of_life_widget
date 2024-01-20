# Conways_game_of_life_widget
[![GitHub release](https://img.shields.io/github/release/ZyMa-1/Conways_game_of_life_widget.svg?style=for-the-badge&logo=github)](https://github.com/ZyMa-1/Conways_game_of_life_widget/releases/latest)
<br>
<br>
[![Python Version](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/downloads/release/python-310/)
[![Licence MIT](https://img.shields.io/badge/License-MIT-purple.svg)](/LICENCE)
![Test Status](https://github.com/ZyMa-1/Conways_game_of_life_widget/actions/workflows/tests.yml/badge.svg?branch=master)

Custom widget made using PySide6 and Python 3.10 version.  
Integratable with Qt Designer.  
  
The project includes a ConfigManager that enables the saving of game widget properties to a JSON file and subsequently loading them back into a widget.  
  
The project also includes a PropertiesManager that facilitates communication between widgets and game widget properties, ensuring that any changes made to one are appropriately reflected in the other.

Goal of the project was to learn how to build scalable and manageble application.
  
# Info
- [Main.md](/info/Main.md)
- [Build.md](/info/Build.md)
- [Localization.md](/info/Localization.md)
- [Resources.md](/info/Resources.md)

# Showcase  
  
Screenshots of the 'MainWindow' and QtDesigner interface, showcasing the loaded plugin, contains in [/readme_images](/readme_images) directory.

Version 0.4 screenshot:

![Image 4](/readme_images/4_new.png)

# Blog

I have written a detailed blog covering all aspects of the application. You can(not) find it [right here](https://zyma-1.github.io/technical/2023/06/26/Conways-game-of-life-as-a-PySide6-widget.html).

# Thanks to qtforpython-6 documentation:
 1. https://doc.qt.io/qt-6/designer-using-custom-widgets.html
 2. https://doc.qt.io/qtforpython-6/deployment/index.html

And there is much more useful information there.
