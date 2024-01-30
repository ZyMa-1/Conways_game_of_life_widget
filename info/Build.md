# Building with Nuitka (v 1.6.6)
Building not complicated PySide project with Nuitka is straightforward.

Install nuitka in your venv:
```bash
pip3 install nuitka
```

**Building standalone:**  

Executing the nuitka with `--standalone` flag will generate two directories: `main.build/` and `main.dist/`.   
The dist directory holds the executable file and other necessary components of the application.
<br>

*Full command for standalone*:
```bash
nuitka --standalone --quiet --disable-console --enable-plugin=pyside6 --output-filename=conways_game_of_life_v0.6.exe .\main.py
```

### Notes on flags:
- `--include-data-dir` Includes data directory to the distribution.
- `--follow-imports` Enabled by default for standalone. Descends into all imported modules.
- `--enable-plugin=pyside6` Required by the PySide6 package for standalone mode.
