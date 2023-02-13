# Copyright (c) 2022 Ultimaker B.V.
# Cura is released under the terms of the LGPLv3 or higher. #\

from Cura.cura import CuraApplication
from Uranium.UM.View import View
from Uranium.UM.Logger import Logger

try:
    from . import ThreeMFReader
    from . import ThreeMFWorkspaceReader
except ImportError:
    Logger.log("w", "Could not import ThreeMFReader and ThreeMFWorkspaceReader; libSavitar may be missing")

class GuiReader:

    def __init__(self, metaData, path):
        self.metaData = {}
        self.path = path


    def getMetaData(self, metadata):

        for key, attr in enumerate(metadata):
            attribute_value = attr[key]
            if attribute_value:
                self.metadata = attribute_value