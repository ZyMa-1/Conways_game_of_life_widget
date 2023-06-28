# Localization:

Create ".ts" file using *pyside6-lupdate* tool:

```
pyside6-lupdate main.py .\src\ .\src\backend\ImageSaver.py .\src\backend\MessageBoxFactory.py .\src\backend\WarningMessageBoxGenerator.py -ts .\localization\translations\main_gui_ru.ts
```

Open ".ts" file using Qt-Linguist tool, do translations and save the result:

```
pyside6-linguist
```

Convert resulted ".ts" files to ".qm" files using *pyside6-lrelease* tool:

```
pyside6-lrelease .\localization\translations\main_gui_ru.ts -qm .\localization\translates\main_gui_ru.qm
pyside6-lrelease .\localization\translations\main_gui_ru.ts -qm .\src\resources_qrc\translations\main_gui_ru.qm
```

Don't forget to do 'Resources.md' next, as qtforpython documentation recommends to hold ".qm" files in Qt Resource system.
