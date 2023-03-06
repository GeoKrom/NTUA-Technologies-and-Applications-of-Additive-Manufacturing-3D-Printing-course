import sys
import zipfile
import xml.etree.cElementTree as ET


from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QListWidget
)
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt

class Window(QMainWindow):

    def __init__(self, file) -> None:
        super(Window, self).__init__()
        self.file = file
        self.setWindowTitle(".3mf File Metadata Reader")

        widget = QListWidget()
        list = readMetadataList(file)

        widget.addItems(list)

        widget.currentItemChanged.connect(self.index_changed)
        widget.currentTextChanged.connect(self.text_changed)

        self.setCentralWidget(widget)


    def index_changed(self, i): # Not an index, i is a QListWidgetItem
        print(i.text())

    def text_changed(self, s): # s is a str
        print(s)



def readMetadataList(file):
    archive = zipfile.ZipFile(file, "r")
    xml_document = archive.open("3D/3dmodel.model")
    archive.close()

    tree = ET.parse(xml_document)

    root = tree.getroot()

    listMetadata = {}
    lst = []
    xmlns = "{http://schemas.microsoft.com/3dmanufacturing/core/2015/02}"

    for data in root.findall(xmlns+'metadata'):

        for k in data.attrib:
            listMetadata[data.attrib[k]] = data.text 

    for i in listMetadata.keys():
            lst.append(i + ": " + listMetadata[i])
    return lst



if __name__ == "__main__":
    app = QApplication(sys.argv)
    args = sys.argv
    
    ThreeMFFile = args[1]
    if ThreeMFFile.endswith(".3mf"):
        w = Window(ThreeMFFile)
        w.show()
        app.exec()
    else:
        print("Error: Wrong type of file!")
        sys.exit()
