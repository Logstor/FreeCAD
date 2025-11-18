# SPDX-License-Identifier: LGPL-2.1-or-later

# (c) 2023 Werner Mayer LGPL

__title__="Document handling module"
__author__ = "Werner Mayer"
__url__ = "https://www.freecad.org"
__doc__ = "Tools for extracting or creating project files"


import os
import xml.sax
import xml.sax.handler
import xml.sax.xmlreader
import zipfile

# SAX handler to parse the Document.xml
class DocumentHandler(xml.sax.handler.ContentHandler):
    """ Parse content of Document.xml or GuiDocument.xml """
    def __init__(self, dirname):
        """ Init parser """
        super().__init__()
        self.files = []
        self.dirname = dirname

    def startElement(self, name, attrs):
        item = attrs.get("file")
        if item is not None:
            self.files.append(os.path.join(self.dirname, str(item)))

    def characters(self, content):
        return

    def endElement(self, name):
        return

def extractDocument(filename, outpath):
    """Extract files from project archive.
    
    Args:
        filename: Path to the FreeCAD project archive (.FCStd file)
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
    """Create project archive.
    
    Args:
        filename: Path to the Document.xml file
        outpath: Path where the project archive (.FCStd file) will be created
    """
    files = getFilesList(filename)
    dirname = os.path.dirname(filename)
    guixml = os.path.join(dirname, "GuiDocument.xml")
    if os.path.exists(guixml):
        files.extend(getFilesList(guixml))
    with zipfile.ZipFile(outpath, "w", zipfile.ZIP_DEFLATED) as compress:
        for file in files:
            if os.path.isfile(file):
                path_in_archive = os.path.relpath(path=file, start=dirname)
                compress.write(file, path_in_archive, zipfile.ZIP_DEFLATED)

def getFilesList(filename):
    """Determine list of files referenced in a Document.xml or GuiDocument.xml.
    
    Args:
        filename: Path to Document.xml or GuiDocument.xml file
        
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
    return files
