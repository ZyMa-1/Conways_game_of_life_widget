"""
Converts .ui file to .py file using 'pyside6-uic' command line tool
"""
import pathlib
import subprocess as sp
from typing import List

PROJECT_ROOT = pathlib.Path(__file__).absolute().parent.parent


def convert_ui(input_path: pathlib.Path, output_path: pathlib.Path):
    params = ["--no-autoconnection", "--absolute-imports", "--rc-prefix"]
    full_command = f"pyside6-uic {' '.join(params)} {str(input_path)} --output {str(output_path)}"
    exit_code = sp.call(full_command, stdout=sp.PIPE)
    if exit_code == 0:
        print("\033[1;32;40m" + "pyside6-uic success \033[0;37;40m")
    else:
        print("\033[1;31;40m" + "pyside6-uic error \033[0;37;40m")


def convert_rcc(input_path: pathlib.Path, output_path: pathlib.Path):
    full_command = f"pyside6-rcc {str(input_path)} --output {str(output_path)}"
    exit_code = sp.call(full_command, stdout=sp.PIPE)
    if exit_code == 0:
        print("\033[1;32;40m" + "pyside6-rcc success \033[0;37;40m")
    else:
        print("\033[1;31;40m" + "pyside6-rcc error \033[0;37;40m")


def update_ts(py_paths: List[pathlib.Path], output_path: pathlib.Path):
    full_command = f"pyside6-lupdate {' '.join([str(path) for path in py_paths])} -ts {str(output_path)}"
    # print(full_command)
    exit_code = sp.call(full_command, stdout=sp.PIPE)
    if exit_code == 0:
        print("\033[1;32;40m" + "pyside6-lupdate success \033[0;37;40m")
    else:
        print("\033[1;31;40m" + "pyside6-lupdate error \033[0;37;40m")


def convert_ts(input_path: pathlib.Path, output_path: pathlib.Path):
    full_command = f"pyside6-lrelease {str(input_path)} -qm {str(output_path)}"
    exit_code = sp.call(full_command, stdout=sp.PIPE)
    if exit_code == 0:
        print("\033[1;32;40m" + "pyside6-lrelease success \033[0;37;40m")
    else:
        print("\033[1;31;40m" + "pyside6-lrelease error \033[0;37;40m")


if __name__ == "__main__":
    src = PROJECT_ROOT / "src"
    designer = PROJECT_ROOT / "designer"
    ui = PROJECT_ROOT / "src" / "ui"
    resources = PROJECT_ROOT / "src" / "resources"
    translations = PROJECT_ROOT / "localization" / "translations"
    r_translations = PROJECT_ROOT / "src" / "resources" / "translations"
    ################## UI ######################################

    input_path_1 = designer / "ConwaysGameOfLifeDialog.ui"
    output_path_1 = ui / "Ui_ConwaysGameOfLifeDialog.py"

    input_path_2 = designer / "MainWindow.ui"
    output_path_2 = ui / "Ui_MainWindow.py"

    input_path_3 = designer / "AboutDialog.ui"
    output_path_3 = ui / "Ui_AboutDialog.py"

    input_path_4 = designer / "InstructionsDialog.ui"
    output_path_4 = ui / "Ui_InstructionsDialog.py"

    convert_ui(input_path_1, output_path_1)
    convert_ui(input_path_2, output_path_2)
    convert_ui(input_path_3, output_path_3)
    convert_ui(input_path_4, output_path_4)

    ################## LOCALIZATION UPDATE ######################################

    main_py = PROJECT_ROOT / "main.py"
    py_paths_1 = [main_py, designer, src]

    output_path_1 = translations / "main_gui_ru.ts"

    update_ts(py_paths_1, output_path_1)

    ################## LOCALIZATION CONVERT #####################################

    input_path_1 = translations / "main_gui_ru.ts"
    output_path_1 = r_translations / "main_gui_ru.qm"

    convert_ts(input_path_1, output_path_1)

    ################## RESOURCES ######################################

    input_path_1 = resources / "resources.qrc"
    output_path_1 = resources / "rc_resources.py"

    convert_rcc(input_path_1, output_path_1)
