"""
Converts .ui file to .py file using 'pyside6-uic' command line tool

Author: ZyMa-1
"""

import pathlib
import subprocess as sp

PROJECT_ROOT = pathlib.Path(__file__).absolute().parent.parent


def convert(input_path: pathlib.Path, output_path: pathlib.Path):
    exit_code = sp.call(f"pyside6-uic  {str(input_path)} --output {str(output_path)}", stdout=sp.PIPE)
    if exit_code == 0:
        print("\033[1;32;40m" + "uic success \033[0;37;40m")
    else:
        print("\033[1;31;40m" + "uic error \033[0;37;40m")


if __name__ == "__main__":
    input_path_1 = PROJECT_ROOT / "src/designer" / "ConwaysGameOfLifeDialog.ui"
    output_path_1 = PROJECT_ROOT / "src/ui" / "Ui_ConwaysGameOfLifeDialog.py"

    input_path_2 = PROJECT_ROOT / "src/designer" / "MainWindow.ui"
    output_path_2 = PROJECT_ROOT / "src/ui" / "Ui_MainWindow.py"

    input_path_3 = PROJECT_ROOT / "src/designer" / "AboutDialog.ui"
    output_path_3 = PROJECT_ROOT / "src/ui" / "Ui_AboutDialog.py"

    convert(input_path_1, output_path_1)
    convert(input_path_2, output_path_2)
    convert(input_path_3, output_path_3)
