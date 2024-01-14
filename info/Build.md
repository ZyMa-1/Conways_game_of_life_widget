# Building with Nuitka (v 1.6.6)
Building not complicated PySide project with Nuitka is straightforward.

Install nuitka in your venv:
```bash
pip3 install nuitka
```

**Building standalone:**  

Run following command:
```bash
nuitka --standalone --follow-imports --quiet --disable-console --plugin-enable=pyside6 --output-filename=conways_game_of_life_v0.2.2.exe .\main.py
```
Executing this command will generate two directories: `main.build/` and `main.dist/`. The dist directory holds the executable file and other necessary components of the application.
<br>  
**Building one file:** (not working with keeping dynamic resources)
<br>
Run following command:
```bash
nuitka --onefile --follow-imports --quiet --disable-console --plugin-enable=pyside6 --output-filename=conways_game_of_life_v0.2.2.exe .\main.py
```
This will create `main.oneilfe-build/` directory and an executable file in a project root directory.

<br>

P.S. to add certain directories with some data to the project build use `--include-data-dir` parameter.

*Full command for standalone*:
```bash
nuitka --include-data-dir=.\pattern_gallery\=.\pattern_gallery\ --standalone --follow-imports --quiet --disable-console --plugin-enable=pyside6 --output-filename=conways_game_of_life_v0.2.2.exe .\main.py
```

*Full command for onefile*:
```bash
nuitka --include-data-dir=.\pattern_gallery\=.\pattern_gallery\ --onefile --follow-imports --quiet --disable-console --plugin-enable=pyside6 --output-filename=conways_game_of_life_v0.2.2.exe .\main.py
```

### Notes:
- `--include-data-dir` works as expected.