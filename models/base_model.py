#!/usr/bin/python3
"""This script is the base model"""
import uuid
import datetime
from models import storage


class BaseModel():
    ''''Class from which all other classes will inherit'''

    def __init__(self, *args, **kwargs):
        '''Initializes instance attributes'''

        if len(kwargs) == 0:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.datetime.now()
            self.updated_at = datetime.datetime.now()
            storage.new(self)
        else:
            for key in kwargs.keys():
                # check and escape the __class__ key
                if key == "__class__":
                    continue
                else:
                    # check and change the format for updated_at & created_at
                    if key == "updated_at" or key == "created_at":
                        kwargs[key] = datetime.datetime.strptime(
                            kwargs[key], "%Y-%m-%dT%H:%M:%S.%f")
                    # set the attributes of the instance
                    setattr(self, key, kwargs[key])
                # self.key = kwargs[key]
                # print(f"{key}: {kwargs[key]}")

    def __str__(self):
        '''Returns official string representation'''
        return (f"[{self.__class__.__name__}] ({self.id}) \
{str(self.__dict__)}")

    def save(self):
        '''updates the public instance attribute updated_at'''
        storage.save()
        self.updated_at = datetime.datetime.now()

    def to_dict(self):
        '''returns a dictionary containing all keys/values of __dict__'''
        object_dict = {}
        for key in self.__dict__.keys():
            if key not in ('created_at', 'updated_at'):
                object_dict[key] = self.__dict__[key]
            else:
                object_dict[key] = datetime.datetime.isoformat(
                    self.__dict__[key])
        object_dict['__class__'] = self.__class__.__name__
        return (object_dict)
