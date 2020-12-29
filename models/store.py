from models.model import Model
from typing import Dict
from dataclasses import dataclass, field
import uuid, re

@dataclass(eq=False)
class Store(Model):
    collection: str = field(init=False, default="stores")
    name: str
    url_prefix: str # https://johnlewis.com/
    tag_name: str
    query: Dict
    _id: str = field(default_factory=lambda : uuid.uuid4().hex)

    def json(self) ->Dict:
        return {
            "_id": self._id,
            "name": self.name,
            "url_prefix": self.url_prefix,
            "tag_name": self.tag_name,
            "query": self.query
            }

    @classmethod
    def get_by_name(cls, store_name: str) -> "Store":  #Store.get_by_name("John Lewis")
        return cls.find_one_by("name", store_name)

    @classmethod
    def get_by_url_prefix(cls, url_prefix: str) -> "Store":
        url_regex = {"$regex": "^{}".format(url_prefix)} # $regex says regular expression validation by mongoDB while searching for  "^{}".format(url_prefix)  i.e make usre that it starts with the url prefix
        return cls.find_one_by("url_prefix", url_regex)

    @classmethod
    def find_by_url(cls, url: str) -> "Store":
        """
        Returns a store from a url like "https://www.johnlewis.com/item/sdfj45h5g4g21k.html"
        : param url: The item's URL
        : return : a Store object that matches the starting part "https://www.johnlewis.com/" of  the URL
        """
        pattern = re.compile(r"(https?://.*?/)")
        match = pattern.search(url)
        url_prefix = match.group(1)
        return cls.get_by_url_prefix(url_prefix)