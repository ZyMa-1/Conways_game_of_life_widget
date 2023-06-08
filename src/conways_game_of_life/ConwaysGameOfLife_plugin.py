"""
Dynamic plugin file with some custom properties.

Author: ZyMa-1
"""

from PySide6.QtDesigner import (QDesignerCustomWidgetInterface)
from PySide6.QtGui import QIcon

from .ConwaysGameOfLife import ConwaysGameOfLife, DEFAULT_COLS, DEFAULT_ROWS, DEFAULT_TURN_DURATION, \
    DEFAULT_BORDER_THICKNESS, DEFAULT_BORDER_COLOR, DEFAULT_CELL_ON_COLOR, DEFAULT_CELL_OFF_COLOR
from .ConwaysGameOfLife_taskmenu import ConwaysGameOfLifeTaskMenuFactory

min_w = 322
min_h = 322

DOM_XML = f"""
<ui language='c++'>
    <widget class='ConwaysGameOfLife' name='conwaysGameOfLife'>
        <property name='geometry'>
            <rect>
                <x>0</x>
                <y>0</y>
                <width>{min_w}</width>
                <height>{min_h}</height>
            </rect>
        </property>
        <property name='cols'>
            <number>{DEFAULT_COLS}</number>
        </property>
        <property name='rows'>
            <number>{DEFAULT_ROWS}</number>
        </property>
        <property name='turn_duration'>
            <number>{DEFAULT_TURN_DURATION}</number>
        </property>
        <property name='border_thickness'>
            <number>{DEFAULT_BORDER_THICKNESS}</number>
        </property>
        <property name='border_color'>
            <color>
                <red>{DEFAULT_BORDER_COLOR.red()}</red>
                <green>{DEFAULT_BORDER_COLOR.green()}</green>
                <blue>{DEFAULT_BORDER_COLOR.blue()}</blue>
            </color>
        </property>
        <property name='cell_dead_color'>
            <color>
                <red>{DEFAULT_CELL_OFF_COLOR.red()}</red>
                <green>{DEFAULT_CELL_OFF_COLOR.green()}</green>
                <blue>{DEFAULT_CELL_OFF_COLOR.blue()}</blue>
            </color>
        </property>
        <property name='cell_alive_color'>
            <color>
                <red>{DEFAULT_CELL_ON_COLOR.red()}</red>
                <green>{DEFAULT_CELL_ON_COLOR.green()}</green>
                <blue>{DEFAULT_CELL_ON_COLOR.blue()}</blue>
            </color>
        </property>
    </widget>
</ui>
"""


class ConwaysGameOfLifePlugin(QDesignerCustomWidgetInterface):
    def __init__(self):
        super().__init__()
        self._form_editor = None

    def createWidget(self, parent):
        t = ConwaysGameOfLife(parent)
        return t

    def domXml(self):
        return DOM_XML

    def group(self):
        return 'My Custom Widgets'

    def icon(self):
        return QIcon()

    def includeFile(self):
        return 'src/conways_game_of_life/ConwaysGameOfLife'

    def initialize(self, form_editor):
        self._form_editor = form_editor
        manager = form_editor.extensionManager()
        iid = ConwaysGameOfLifeTaskMenuFactory.task_menu_iid()
        manager.registerExtensions(ConwaysGameOfLifeTaskMenuFactory(manager), iid)

    def isContainer(self):
        return False

    def isInitialized(self):
        return self._form_editor is not None

    def name(self):
        return 'ConwaysGameOfLife'

    def toolTip(self):
        return 'Conways Game Of Life widget'

    def whatsThis(self):
        return self.toolTip()
