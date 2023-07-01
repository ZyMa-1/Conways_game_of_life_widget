# Localization:

Create ".ts" file using *pyside6-lupdate* tool:

```
pyside6-lupdate {src_directory} {designer_directory(with ui files)} -ts {path_to_output_ts file}
```
<br>
Open ".ts" file using Qt-Linguist tool, do translations there and save the result:

```bash
pyside6-linguist
```
<br>
Convert resulted ".ts" files to ".qm" files using *pyside6-lrelease* tool:

```
pyside6-lrelease {ts_file_path} -qm {qm_file_path}
```

Don't forget to do 'Resources.md' next, as qtforpython documentation recommends to hold ".qm" files in Qt Resource system.
And my project does so.
