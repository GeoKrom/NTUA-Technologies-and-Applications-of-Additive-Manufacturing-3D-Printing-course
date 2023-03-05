# Copyright (c) 2022 Ultimaker B.V.
# Cura is released under the terms of the LGPLv3 or higher. #\

from Cura.cura import CuraApplication
from Uranium.UM import  Extension
import sys
import os
from PyQt6.QtWidgets import *
from Uranium.UM.View import View
from Uranium.UM.Logger import Logger
from Uranium.UM.PluginRegistry import PluginRegistry
try:
    from . import ThreeMFReader
    from . import ThreeMFWorkspaceReader
except ImportError:
    Logger.log("w", "Could not import ThreeMFReader and ThreeMFWorkspaceReader; libSavitar may be missing")

class MetadataReader(PluginRegistry):

    def __init__(self, _metadata, path_file):
        super().__init__()
        self._metadata = {}
        self._path_file = path_file
        self._file = os.path.basename(path_file)

    def checkFile(self, _file):
        if not _file.endswith(".3mf"):
            return False

    def readMetadata(self, _metadata: dict) -> dict:

        for key, attr in enumerate(_metadata):
            attribute_value = attr[key]
            if attribute_value:
                self._metadata = attribute_value

        return _metadata



class GuiMetadataReader(Extension, View):

    def __init__(self, metadata: dict) -> None:
        super().__init__()
        self.metadata = MetadataReader.readMetadata(metadata)

    def getMetadata(self, metadata: dict) -> dict:
        return metadata

    def projectMetadata(self, metadata: dict) -> list:
        attr_val = []

        for key, attr in enumerate(metadata):
            attr_val = attr[key]
        return attr_val

    def clicked(self, qmodelindex):
        item = self.listWidget.currentItem()
        print(item.text())

    def openWindow(self):

        self.window = QWidget()
        self.window.resize(500,500)
        self.window.move(100,100)
        self.window.setWindowTitle('.3mf File Metadata ')
        self.layout = QGridLayout()
        self.listMetadata = GuiMetadataReader.projectMetadata()
        self.listWidget  = QListWidget()

        for i in range(0,len(self.listMetadata)):
            self.listWidget.insertItem(i+1, self.listMetadata[i])

        self.listWidget.clicked.connect(self.clicked)
        self.layout.addWidget(self.listWidget)


        self.window.show()