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
    ################## UI ######################################

    input_path_1 = PROJECT_ROOT / "designer" / "ConwaysGameOfLifeDialog.ui"
    output_path_1 = PROJECT_ROOT / "src" / "ui" / "Ui_ConwaysGameOfLifeDialog.py"

    input_path_2 = PROJECT_ROOT / "designer" / "MainWindow.ui"
    output_path_2 = PROJECT_ROOT / "src" / "ui" / "Ui_MainWindow.py"

    input_path_3 = PROJECT_ROOT / "designer" / "AboutDialog.ui"
    output_path_3 = PROJECT_ROOT / "src" / "ui" / "Ui_AboutDialog.py"

    input_path_4 = PROJECT_ROOT / "designer" / "InstructionsDialog.ui"
    output_path_4 = PROJECT_ROOT / "src" / "ui" / "Ui_InstructionsDialog.py"

    convert_ui(input_path_1, output_path_1)
    convert_ui(input_path_2, output_path_2)
    convert_ui(input_path_3, output_path_3)
    convert_ui(input_path_4, output_path_4)

    ################## LOCALIZATION UPDATE ######################################

    src_path = PROJECT_ROOT / "src"
    designer_path = PROJECT_ROOT / "designer"
    main_py_path = PROJECT_ROOT / "main.py"
    py_paths_1 = [main_py_path, designer_path, src_path]

    output_path_1 = PROJECT_ROOT / "localization" / "translations" / "main_gui_ru.ts"

    update_ts(py_paths_1, output_path_1)

    ################## LOCALIZATION CONVERT #####################################

    input_path_1 = PROJECT_ROOT / "localization" / "translations" / "main_gui_ru.ts"
    output_path_1 = PROJECT_ROOT / "src" / "resources" / "translations" / "main_gui_ru.qm"

    convert_ts(input_path_1, output_path_1)

    ################## RESOURCES ######################################

    input_path_1 = PROJECT_ROOT / "src" / "resources" / "resources.qrc"
    output_path_1 = PROJECT_ROOT / "src" / "resources" / "rc_resources.py"

    convert_rcc(input_path_1, output_path_1)