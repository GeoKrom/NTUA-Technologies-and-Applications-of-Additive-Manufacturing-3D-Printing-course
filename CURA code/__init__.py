from typing import Dict
import sys
from Uranium.UM.i18n import i18nCatalog
from Uranium.UM.Logger import Logger
catalog = i18nCatalog("cura")
try:
    from . import GuiReader
except ImportError:
    Logger.log("w", "Could not import ThreeMFReader; libSavitar may be missing")


def getMetaData() -> Dict:
    metaData = {}
    workspace_extension = "3mf"

    if "3MFGuiReader.GuiReader"  in sys.modules:


            metaData["file_metadata_reader"] = [
                    {
                        "extension": ".3mf",
                        "description": catalog.i18nc("@item:inlistbox", "3MF File")
                    }
            ]
            metaData["project_metadata"] = [
                {
                    "extension": workspace_extension,
                    "description": catalog.i18nc("@item:inlistbox", "3MF File")
                }
            ]


    return metaData

def register(app):

    if "3MFGuiReader.GuiReader"  in sys.modules:

        return {"file_metadata_reader": GuiReader.GuiMetadataReader(),
                "project_metadata": GuiReader.GuiMetadataReader()}
    else:
        return  {}