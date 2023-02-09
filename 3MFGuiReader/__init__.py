from . import GuiReader


def getMetaData():
    return {}


def register(app):
    return {"extesion": GuiReader.GuiReader()}
