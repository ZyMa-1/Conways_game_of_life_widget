# Resources

To convert resources (.qrs) files to python (.py) files use *pyside6-rcc* tool:

```
pyside6-rcc {qrc_file_path} -o {py_file_path}
```

To use resources, import resulted file into "main.py" file and make sure import would not be removed by IDE formatting.

Or else resources can be imported by adding ".qrc" file into Qt-Designer, which will then
automatically import it in ".ui" file, distributing it across the project.
