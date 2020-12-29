from abc import ABCMeta, abstractmethod
from typing import Dict, List, TypeVar, Type, Union
from common.database import Database

# allow us to define custom types (cls) 'T' here like for eg: List[str]. A variable bound to a specific class but will still work with subclasses i.e Item and Alert here. The type matches the caller class.
T = TypeVar('T', bound="Model")

class Model(metaclass=ABCMeta):
    collection: str
    _id: str #works both for instance properties and class properties

    def __init__(self, *arg, **kwargs):
        pass

    def save_to_mongo(self):
        Database.update(self.collection, {"_id": self._id}, self.json())

    def remove_from_mongo(self):
        Database.remove(self.collection, {"_id": self._id})

    @abstractmethod
    def json(self) -> Dict:
        raise NotImplementedError

    @classmethod
    def get_by_id(cls: Type[T], _id: str) -> T: # returns type of the class that called this method Item.get_by_id() ->  Item, Alert.get_by_id() -> Alert
        return cls.find_one_by("_id", _id) #returns an item object  or alert object made with the contents of the thing that was found in the database

    @classmethod
    def all(cls: Type[T]) -> List[T]:
        elements_from_db = Database.find(cls.collection, {})
        return [cls(**elem) for elem in elements_from_db] # returns a set/list of alert objects

    @classmethod
    def find_one_by(cls: Type[T], attribute: str, value: Union[str, Dict]) -> T: #Item.find_one_by('url', 'http://bla.com') returns a single element/object
        return cls(**Database.find_one(cls.collection, {attribute: value}))

    @classmethod
    def find_many_by(cls: Type[T], attribute: str, value: Union[str, Dict]) ->List[T]: #returns a list of objects 
        return [cls(**elem) for elem in Database.find(cls.collection, {attribute: value})]