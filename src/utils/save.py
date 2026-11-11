"""
Date : 11/11/2026
Author : Tao Serveaux

Description :
    Persistence layer. The Save class writes and reads the inventory data in a
    JSON file, and keeps a copy of the component pictures in a "pictures" folder.
    It knows nothing about components or quantities: it only stores what it is given.
"""

import json
import os
import shutil
import uuid


class Save:
    """
    Description : Reads / writes the data file and stores the pictures.
    """

    def __init__(self, fileName, path):
        """
        Description : Build the paths and create the data and pictures folders if needed.

        Args :
            fileName (str) : name of the JSON file (e.g. "inventory.json").
            path (str) : folder where the data is stored.

        Output :
            None
        """

        self.__path = os.path.join(path, fileName)
        self.__picturesFolder = os.path.join(path, "pictures")
        os.makedirs(self.__picturesFolder, exist_ok=True)

    def saveData(self, data):
        """
        Description : Write the data in the JSON file, safely.
            The data is first written into a temporary file, which then replaces
            the real file in one step: if the program crashes while writing,
            the previous save stays intact.

        Args :
            data (dict) : the data to save (must be convertible to JSON).

        Output :
            None
        """

        temporaryPath = self.__path + ".tmp"

        with open(temporaryPath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        os.replace(temporaryPath, self.__path)

    def loadData(self):
        """
        Description : Read the JSON file.

        Args :
            None

        Output :
            dict | None : the saved data, or None on the first launch (no file yet).

        Raises :
            json.JSONDecodeError : the file exists but is not valid JSON.
        """

        if not os.path.exists(self.__path):
            return None

        with open(self.__path, encoding="utf-8") as f:
            return json.load(f)

    def storePicture(self, sourcePath):
        """
        Description : Copy a picture into the pictures folder under a unique name,
            so the original file can be moved or deleted without breaking the inventory.

        Args :
            sourcePath (str) : path of the original picture.

        Output :
            str : file name of the copy (not the full path).

        Raises :
            OSError : the picture could not be copied (missing file, no permission...).
        """

        extension = os.path.splitext(sourcePath)[1].lower()
        fileName = uuid.uuid4().hex + extension
        shutil.copy2(sourcePath, os.path.join(self.__picturesFolder, fileName))

        return fileName

    def picturePath(self, fileName):
        """
        Description : Give the full path of a stored picture.

        Args :
            fileName (str) : file name returned by storePicture.

        Output :
            str : full path of the picture.
        """

        return os.path.join(self.__picturesFolder, fileName)
