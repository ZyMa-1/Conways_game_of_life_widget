# Building with Nuitka (v 1.6.6)
Building not complicated PySide project with Nuitka is straightforward.

Install nuitka in your venv:
```
pip3 install nuitka
```

**Building standalone:**  

Run following command:
```
nuitka --standalone --follow-imports --quiet --disable-console --plugin-enable=pyside6 --output-filename=conways_game_of_life.exe .\main.py
```
Executing this command will generate two directories: `main.build/` and `main.dist/`. The dist directory holds the executable file and other necessary components of the application.
<br>  
**Building one file:**  
<br>
Run following command:
```
nuitka --onefile --follow-imports --quiet --disable-console --plugin-enable=pyside6 --output-filename=conways_game_of_life.exe .\main.py
```
This will create `main.oneilfe-build/` directory and an executable file in a project root directory.
