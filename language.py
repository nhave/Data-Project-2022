import json

class Lang:
    def __init__(self, jsonFile, language):
        self.__jsonFile = jsonFile
        self.__load(language)
    
    def __load(self, language):
        try:
            with open(self.__jsonFile, 'r', encoding='utf8') as f:
                conf = json.load(f)
                if type(conf.get(language)) == dict:
                    self.__lang = conf.get(language)
        except:
            self.__lang = {}
        pass

    def setLanguage(self, language):
        self.__load(language)

    def translate(self, value):
        try:
            out = self.__lang.get(value)
            if(len(out) < 1):
                out = value
            return out
        except:
            return value
        pass