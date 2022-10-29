#!/usr/bin/python3
"""This module is the file storage class"""
import json
import os
import datetime


class FileStorage():
    """Class for storing and retrieving data"""
    __file_path = "file.json"
    __objects = {}

    # def __init__(self):
    #     pass

    def all(self):
        '''returns the dictionary __objects'''
        return self.__objects

    def new(self, obj):
        '''sets in __objects the obj with key <obj class name>.id'''
        objname = obj.__class__.__name__
        objID = obj.id
        key = f"{objname}.{objID}"  # <class name>.id = obj
        self.__objects[key] = obj

    def save(self):
        ''' serializes __objects to the JSON file (path: __file_path)'''
        # serialize the object by first converting it to a dictionary
        object_dict = {}

        for key in self.__objects.keys():
            if type(self.__objects[key]) != dict:
                object_dict[key] = self.__objects[key].to_dict()
        # convert the dictionary object to json and write to the file
        file_name = self.__file_path
        with open(file_name, "w", encoding="utf-8") as jsonfile:
            # json.dump(object_dict, jsonfile)
            jsonfile.write(json.dumps(object_dict))

    def classes(self):
        """Returns a dictionary of valid classes and their references."""
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        classes = {"BaseModel": BaseModel,
                   "User": User,
                   "State": State,
                   "City": City,
                   "Amenity": Amenity,
                   "Place": Place,
                   "Review": Review
                   }
        return classes

    def reload(self):
        """Reloads the stored objects"""
        if os.path.exists(FileStorage.__file_path):
            #  load the file and dump content as dictionary
            with open(FileStorage.__file_path, "r", encoding="utf-8") \
                    as my_file:
                object_dict = json.loads(my_file.read())
            final_dict = {}

            for id, dictionary in object_dict.items():
                class_name = dictionary['__class__']
                final_dict[id] = self.classes()[class_name](**dictionary)
            FileStorage.__objects = final_dict

    def attributes(self):
        """Returns the valid attributes and their types for classname."""
        attributes = {
            "BaseModel":
                     {"id": str,
                      "created_at": datetime.datetime,
                      "updated_at": datetime.datetime},
            "User":
                     {"email": str,
                      "password": str,
                      "first_name": str,
                      "last_name": str},
            "State":
                     {"name": str},
            "City":
                     {"state_id": str,
                      "name": str},
            "Amenity":
                     {"name": str},
            "Place":
                     {"city_id": str,
                      "user_id": str,
                      "name": str,
                      "description": str,
                      "number_rooms": int,
                      "number_bathrooms": int,
                      "max_guest": int,
                      "price_by_night": int,
                      "latitude": float,
                      "longitude": float,
                      "amenity_ids": list},
            "Review":
            {"place_id": str,
                         "user_id": str,
                         "text": str}
        }
        return attributes
