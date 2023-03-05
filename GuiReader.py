# Copyright (c) 2022 Ultimaker B.V.
# Cura is released under the terms of the LGPLv3 or higher. #\

from Cura.cura import CuraApplication
from Uranium.UM import  Extension
import os
from PyQt6.QtCore import Qt, QAbstractItemModel, QModelIndex, QVariant, pyqtProperty, pyqtSignal, pyqtSlot
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

    def checkFile(self, file):
        if not file.endswith(".3mf"):
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
        self.metadata = MetadataReader.getMetadata(metadata)

    def getMetadata(self, _metadata: dict) -> dict:
        return _metadata

    def openWindow(self):
        pass

    def projectMetadata(self, metadata: dict):
        pass
