#! python
# SPDX-License-Identifier: LGPL-2.1-or-later

# (c) 2010 Werner Mayer LGPL
# FreeCAD Python script to work with the FCStd file format.

import os
import xml.sax
import xml.sax.handler
import xml.sax.xmlreader
import zipfile


# SAX handler to parse the Document.xml
class DocumentHandler(xml.sax.handler.ContentHandler):
    def __init__(self, dirname):
        super().__init__()
        self.files = []
        self.dirname = dirname

    def startElement(self, name, attributes):
        item = attributes.get("file")
        if item is not None:
            self.files.append(os.path.join(self.dirname, str(item)))

    def characters(self, data):
        return

    def endElement(self, name):
        return


def extractDocument(filename, outpath):
    """Extract a FreeCAD document (.FCStd) file to a directory.
    
    Args:
        filename: Path to the .FCStd file to extract
        outpath: Directory path where files will be extracted
    """
    with zipfile.ZipFile(filename) as zfile:
        files = zfile.namelist()

        for file_path in files:
            data = zfile.read(file_path)
            dirs = file_path.split("/")
            if len(dirs) > 1:
                dirs.pop()
                curpath = outpath
                for dir_name in dirs:
                    curpath = curpath + "/" + dir_name
                    os.mkdir(curpath)
            with open(outpath + "/" + file_path, "wb") as output:
                output.write(data)


def createDocument(filename, outpath):
    """Create a FreeCAD document (.FCStd) file from extracted files.
    
    Args:
        filename: Path to the Document.xml file
        outpath: Path where the .FCStd file will be created
    """
    files = getFilesList(filename)
    with zipfile.ZipFile(outpath, "w", zipfile.ZIP_DEFLATED) as compress:
        for file_path in files:
            dirs = os.path.split(file_path)
            # print file_path, dirs[-1]
            compress.write(file_path, dirs[-1], zipfile.ZIP_DEFLATED)


def getFilesList(filename):
    """Get list of files referenced in a FreeCAD Document.xml file.
    
    Args:
        filename: Path to the Document.xml file
        
    Returns:
        List of file paths referenced in the document
    """
    dirname = os.path.dirname(filename)
    handler = DocumentHandler(dirname)
    parser = xml.sax.make_parser()
    parser.setContentHandler(handler)
    parser.parse(filename)

    files = []
    files.append(filename)
    files.extend(iter(handler.files))
    gui_doc_path = os.path.join(dirname, "GuiDocument.xml")
    if os.path.exists(gui_doc_path):
        files.append(gui_doc_path)
    return files
