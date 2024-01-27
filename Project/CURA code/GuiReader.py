# Copyright (c) 2022 Ultimaker B.V.
# Cura is released under the terms of the LGPLv3 or higher. #\

from Cura.cura import CuraApplication
from Uranium.UM import  Extension
from PyQt6.QtWidgets import *
from Uranium.UM.View import View
from Uranium.UM.Logger import Logger
from Uranium.UM.PluginRegistry import PluginRegistry
import sys
import os
import zipfile
import xml.etree.cElementTree as ET


from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QListWidget
)
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt

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

    def readMetadata(self) -> dict:

        archive = zipfile.ZipFile(self._file, "r")
        xml_document = archive.open("3D/3dmodel.model")
        archive.close()

        tree = ET.parse(xml_document)

        root = tree.getroot()
        xmlns = "{http://schemas.microsoft.com/3dmanufacturing/core/2015/02}"

        for data in root.findall(xmlns+'metadata'):

            for k in data.attrib:
             self._metadata[data.attrib[k]] = data.text 
        return self._metadata



class GuiMetadataReader(QMainWindow,Extension, View):

    def __init__(self, metadata: dict) -> None:
        super().__init__()
        self.metadata = MetadataReader.readMetadata(metadata)

    def getMetadata(self) -> dict:
        return self.metadata

    def projectMetadata(self) -> list:
        attr_val = []

        for i in self.metadata.keys():
            attr_val.append(i + ": " + self.metadata[i])
        return attr_val

    def clicked(self, qmodelindex):
        item = self.listWidget.currentItem()
        print(item.text())

    def openWindow(self):

        self.setWindowTitle(".3mf File Metadata Reader")
        widget = QListWidget()
        list = GuiMetadataReader.projectMetadata()
        widget.addItems(list)
        widget.currentItemChanged.connect(self.index_changed)
        widget.currentTextChanged.connect(self.text_changed)

        self.setCentralWidget(widget)
        self.window.show()

    def index_changed(self, i): # Not an index, i is a QListWidgetItem
        print(i.text())

    def text_changed(self, s): # s is a str
        print(s)

    