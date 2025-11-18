# SPDX-License-Identifier: LGPL-2.1-or-later

# (c) 2024 Werner Mayer LGPL

__author__ = "Werner Mayer"
__url__ = "https://www.freecad.org"
__doc__ = "Helper module to convert zip files"


import zipfile


def rewrite(source: str, target: str):
    """Rewrite a zip file from source to target.
    
    This function reads all entries from a source zip file and writes them
    to a new target zip file, effectively creating a fresh copy.
    
    Args:
        source: Path to the source zip file
        target: Path to the target zip file to create
    """
    with zipfile.ZipFile(source, "r") as source_zip, zipfile.ZipFile(
        target, "w"
    ) as target_zip:
        for name in source_zip.namelist():
            with source_zip.open(name) as source_file:
                target_zip.writestr(name, source_file.read())
