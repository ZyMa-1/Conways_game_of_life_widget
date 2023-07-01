# Resources

To convert resources (.qrs) files to python (.py) files use *pyside6-rcc* tool:

```
pyside6-rcc {qrc_file_path} -o {py_file_path}
```

To use resources, import it to your "main.py" file and make sure import would not be removed by IDE formatting.

Or else you can add resource ".qrc" file in Qt-Designer, which will then
automatically import it in ".ui" file, distributing it across the project.
