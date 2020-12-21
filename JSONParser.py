#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 19:34:57 2020

@author: nico
"""

from json import load, dumps
from os import makedirs
from os.path import exists

class FileManager:
    
    def __init__(self, work_directory, logger):
        if not exists(work_directory):
            makedirs(work_directory)
        self.work_directory = work_directory + "/"
        self.logger = logger
        self.log("Parser initialized")
    
    # JSON decode and encode *************************************************
    
    def dumps_json(self, obj):
        return dumps(obj)
    
    def decodeJSON(self, file_name):
        self.log(f"Attempting to decode the json file {file_name} to a dictionary")
        try:
            with open(self.work_directory + file_name, "r") as fin:
                dic = load(fin)
                fin.close()
                return dic
        except:
            open(self.work_directory + file_name, "w")
            self.error(f"Could not decode the dictionary from the json file {file_name}")
            return {}
        
    def encodeJSON(self, file_name, dic):
        self.log(f"Attempting to encode {file_name} from a dictionary")
        try:
            with open(self.work_directory + file_name, "w") as fout:
                fout.write(dumps(dic))
                fout.close()
                return None
        except:
            self.error(f"Could not encode the dictionary in the json file {file_name}")
            return "Error"
    
    # ************************************************************************
    # ";\n" separated file encode and decode to array ************************
    
    def decode_to_array(self, file_name, separator=";\n"):
        self.log(f"Attempting to decode file {file_name} to an array")
        try:
            with open(self.work_directory + file_name, "r") as fin:
                arr = fin.read().split(separator)
                self.log(f"{arr}")
                return arr                
        except:
            open(self.work_directory + file_name, "w")
            self.error(f"Could not decode the array from the file {file_name}")
            return []
        
    def encode_from_array(self, file_name, array, separator=";\n"):
        self.log(f"Attempting to encode file {file_name} from an array")
        try:
            with open(self.work_directory + file_name, "w") as fout:
                fout.write(separator.join(array))
                return None
        except:
            self.error(f"Could not encode the array in the file {file_name}")
            return "Error"
    
    # ************************************************************************
    # ";\n" separated file encode and decode value after value
    
    def encode_value(self, file_name, string, separator=";\n"):
        self.log(f"Attempting to add a value to the file {file_name}")
        try:
            with open(self.work_directory + file_name, "a+") as fout:
                fout.write(string)
        except:
            self.error(f"Could not add the value to the file {file_name}")
            return "Error"
    
    # ";\n" separated file divided by - **************************************
    
    def decode_array_double_separator(self, file_name, separator=";\n", separator2="-"):
        self.log(f"Attempting do decode file {file_name} to arrays")
        try:
            with open(self.work_directory + file_name, "r") as fin:
                arr = fin.read().split(separator)
                result = list()
                for element in arr:
                    res = element.split(separator2)
                    try:
                        res.replace(";", "")
                    except:
                        pass
                    result.append(res)
                return result
        except:
            # open(self.work_directory + file_name, "w")
            self.error(f"Could not decode file {file_name} to arrays")
            return []
    
    # ************************************************************************
    # LOGGER *****************************************************************
    
    def log(self, message):
        try:
            self.logger.info(f"[FileParser] {message}")
        except:
            pass
    
    def error(self, message):
        try:
            self.logger.error(f"[FileParser] {message}")
        except:
            pass
    
    
    