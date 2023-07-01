# Resources

To convert resources (.qrs) files to python (.py) files use *pyside6-rcc* tool:

```
pyside6-rcc .\src\resources\resources.qrc -o .\src\resources\rc_resources.py
```

To use resources, import it to your "main.py" file and make sure import would not be removed by IDE formatting.
