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
