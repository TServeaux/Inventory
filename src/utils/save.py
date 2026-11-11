"""
Date : 11/11/2026
Author : Tao Serveaux

Description :
    Persistence layer. The Save class writes and reads the inventory data in a
    JSON file. It knows nothing about components or quantities: it only stores
    what it is given.
"""

import json
import os


class Save:
    """
    Description : Reads / writes the data file.
    """

    def __init__(self, fileName, path):
        """
        Description : Build the path of the file and create the data folder if needed.

        Args :
            fileName (str) : name of the JSON file (e.g. "inventory.json").
            path (str) : folder where the data is stored.

        Output :
            None
        """

        self.__path = os.path.join(path, fileName)
        os.makedirs(path, exist_ok=True)

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

        # "utf-8-sig" also accepts files starting with a BOM (an invisible mark
        # that some Windows editors add at the start of the file).
        with open(self.__path, encoding="utf-8-sig") as f:
            return json.load(f)
