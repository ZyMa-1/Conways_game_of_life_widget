"""
This file registers plugin in QtDesigner.

Author: ZyMa-1
"""

from PySide6.QtDesigner import QPyDesignerCustomWidgetCollection

from src.conways_game_of_life.ConwaysGameOfLife import ConwaysGameOfLife
from src.conways_game_of_life.ConwaysGameOfLife_plugin import ConwaysGameOfLifePlugin

# Set PYSIDE_DESIGNER_PLUGINS to point to this directory and load the plugin
# For unknown reasons, widget registers only when this file is located in the project root

if __name__ == '__main__':
    # with open("asd", "a") as f:
    #     f.write("hello there")
    QPyDesignerCustomWidgetCollection.addCustomWidget(ConwaysGameOfLifePlugin())
