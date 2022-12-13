import os, json

class Config:
    #Initial method to setup the config.
    def __init__(self, jsonFile):
        """"Creates a new configuration.
        
        ``jsonFile`` is the full path of the ``JSON File`` needed.
        
        Using ``"./folder/file.json"`` places the file where the current program is running.
        
        Usin ``"C:/folder/file.json"`` places the file the file at the specific location."""
        self.__jsonFile = jsonFile
        self.__config = {}
        self.__changed = False

        self.__load()
        pass

    #Private funtion tries to load the config from the file.
    def __load(self):
        try:
            with open(self.__jsonFile, 'r', encoding='utf8') as f:
                conf = json.load(f)
                if type(conf) == dict:
                    self.__config = conf
        except:
            pass
        pass

    #Saves the configuration to the config file.
    def save(self):
        """Saves the config to the given file.
        
        If neither ``file`` or ``folder`` exist, they will be created"""
        if self.__changed:
            #Check if file path exists otherwise create it.
            directory = os.path.dirname(self.__jsonFile)
            if not os.path.exists(directory):
                os.makedirs(directory)
            
            with open(self.__jsonFile, 'w', encoding='utf8') as json_file:
                json.dump(self.__config, json_file, indent = 4, sort_keys=True, ensure_ascii=False)
            self.__changed = False
        pass
    
    #Private function to get the value of a key in the config.
    #If the key dont exist or dont match the type, it creates it.
    def __getOrCreate(self, key, value):
        if len(key) == 0:
            raise Exception("String \"key\" cannot be empty!")
        if key[0] == "." or key[len(key) - 1] == ".":
            raise Exception("String \"key\" cannot start or end with \".\"")

        splitString = key.split(".")
        last = splitString[len(splitString) - 1]

        item = self.__config
        for i in range(len(splitString) - 1):
            t = item.get(splitString[i])
            if type(t) != dict:
                t = {}
            item[splitString[i]] = t
            item = item.get(splitString[i])

        if type(item.get(last)) != type(value):
            item[last] = value
            self.__changed = True

        return item.get(last)

    #Private function to set a key in the config.
    def __set(self, key, value):
        if len(key) == 0:
            raise Exception("String \"key\" cannot be empty!")
        if key[0] == "." or key[len(key) - 1] == ".":
            raise Exception("String \"key\" cannot start or end with \".\"")

        splitString = key.split(".")
        last = splitString[len(splitString) - 1]

        item = self.__config
        for i in range(len(splitString) - 1):
            t = item.get(splitString[i])
            if type(t) != dict:
                t = {}
            item[splitString[i]] = t
            item = item.get(splitString[i])

        item[last] = value
        self.__changed =True
        pass

    #Returns an Integer from the config.
    def getInteger(self, key, default, minimum=None, maximum=None):
        """Returns an ``Integer`` from the config.

        ``key`` is the Key read in the config. You can use ``.`` to create Categories and Subcategories but cannot start or end with ``.``

        ``default`` is returned if no matching key is found or if ``minimum=`` or ``maximum=`` is set."""
        if type(default) != int:
            raise TypeError("Key \"default\" must be of type \"int\"")

        result = self.__getOrCreate(key, default)
        if (type(minimum) == int and minimum > result) or (type(maximum) == int and maximum < result):
            self.__set(key, default)
            return default
        else:
            return result

    #Returns a Float from the config.
    def getFloat(self, key, default, minimum=None, maximum=None):
        """Returns a ``Float`` from the config.

        ``key`` is the Key read in the config. You can use ``.`` to create Categories and Subcategories but cannot start or end with ``.``

        ``default`` is returned if no matching key is found or if ``minimum=`` or ``maximum=`` is set."""
        if type(default) != float:
            raise TypeError("Key \"default\" must be of type \"float\"")

        result = self.__getOrCreate(key, default)
        if (type(minimum) == float and minimum > result) or (type(maximum) == float and maximum < result):
            self.__set(key, default)
            return default
        else:
            return result

    #Returns a Boolean from the config.
    def getBoolean(self, key, default):
        """Returns a ``Boolean`` from the config.

        ``key`` is the Key read in the config. You can use ``.`` to create Categories and Subcategories but cannot start or end with ``.``

        ``default`` is returned if no matching key is found."""
        if type(default) != bool:
            raise TypeError("Key \"default\" must be of type \"bool\"")

        return self.__getOrCreate(key, default)

    #Returns a String from the config.
    def getString(self, key, default):
        """Returns a ``String`` from the config.

        ``key`` is the Key read in the config. You can use ``.`` to create Categories and Subcategories but cannot start or end with ``.``

        ``default`` is returned if no matching key is found."""
        if type(default) != str:
            raise TypeError("Key \"default\" must be of type \"str\"")

        return self.__getOrCreate(key, default)

    #Returns a List from the config.
    def getList(self, key, default):
        """Returns a ``List`` from the config.

        ``key`` is the Key read in the config. You can use ``.`` to create Categories and Subcategories but cannot start or end with ``.``

        ``default`` is returned if no matching key is found."""
        if type(default) != list:
            raise TypeError("Key \"default\" must be of type \"list\"")

        return self.__getOrCreate(key, default)

    #Sets the value of an Integer in the config.
    def setInteger(self, key, value, minimum=None, maximum=None):
        """Sets an ``Integer`` in the config.

        ``key`` is the Key to set in the config. You can use ``.`` to create Categories and Subcategories but cannot start or end with ``.``

        ``value`` is the ``Integer`` stored with the key. A ``minimum=`` and ``maximum=`` can be set."""
        if type(value) != int:
            raise TypeError("Key \"value\" must be of type \"int\"")
        if (type(minimum) == int and minimum > value) or (type(maximum) == int and maximum < value):
            raise Exception("Key \"value\" is out of range!")

        self.__set(key, value)
        return value

    #Sets the value of a Float in the config.
    def setFloat(self, key, value, minimum=None, maximum=None):
        """Sets a ``Float`` in the config.

        ``key`` is the Key to set in the config. You can use ``.`` to create Categories and Subcategories but cannot start or end with ``.``

        ``value`` is the ``Float`` stored with the key. A ``minimum=`` and ``maximum=`` can be set."""
        if type(value) != float:
            raise TypeError("Key \"value\" must be of type \"float\"")
        if (type(minimum) == float and minimum > value) or (type(maximum) == float and maximum < value):
            raise Exception("Key \"value\" is out of range!")

        self.__set(key, value)
        return value

    #Sets the value of a Boolean in the config.
    def setBoolean(self, key, value):
        """Sets a ``Boolean`` in the config.

        ``key`` is the Key to set in the config. You can use ``.`` to create Categories and Subcategories but cannot start or end with ``.``

        ``value`` is the ``Boolean`` stored with the key."""
        if type(value) != bool:
            raise TypeError("Key \"value\" must be of type \"bool\"")
        self.__set(key, value)
        return value

    #Sets the value of a String in the config.
    def setString(self, key, value):
        """Sets a ``String`` in the config.

        ``key`` is the Key to set in the config. You can use ``.`` to create Categories and Subcategories but cannot start or end with ``.``

        ``value`` is the ``String`` stored with the key."""
        if type(value) != str:
            raise TypeError("Key \"value\" must be of type \"str\"")
        self.__set(key, value)
        return value

    #Sets the value of a List in the config.
    def setList(self, key, value):
        """Sets a ``List`` in the config.

        ``key`` is the Key to set in the config. You can use ``.`` to create Categories and Subcategories but cannot start or end with ``.``

        ``value`` is the ``List`` stored with the key."""
        if type(value) != list:
            raise TypeError("Key \"value\" must be of type \"list\"")
        self.__set(key, value)
        return value

    #Returns the dictionary for the config itself.
    def getConfig(self):
        """Returns the ``Dictionary`` used in the config.
        
        Mainly used for debugging."""
        return self.__config.copy()
