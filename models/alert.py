from typing import Dict
from models.item import Item
from models.model import Model
from models.user import User
from dataclasses import dataclass, field
from libs.mailgun import Mailgun
import uuid

@dataclass(eq=False) # going to remove all quality generation from the class i.e we will no longer be able to compare alerts as it does not make sense to compare two alerts in our app so inorder to prevent us from accidentally doing that we use eq=False which will give an error when we try to do a compare.
class Alert(Model):
    collection: str = field(init=False, default="alerts") # will not be included in init method and will be default value for all the objects that are created for the Alert class.
    name: str
    item_id: str
    price_limit: float
    user_email: str
    _id: str = field(default_factory=lambda : uuid.uuid4().hex)

    def __post_init__(self):
        self.item = Item.get_by_id(self.item_id)
        self.user = User.find_by_email(self.user_email)

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "name": self.name,
            "item_id": self.item_id,
            "price_limit":self.price_limit,
            "user_email": self.user_email    
        } # the order does not matter as they are passed into the class as named arguements.
        
    def load_item_price(self) -> float:
        self.item.load_price()
        return self.item.price

    def notify_if_price_reached(self):
        if self.item.price < self.price_limit:
            print (f"Item {self.item} has reached a price under {self.price_limit}. Latest price {self.item.price}")
            Mailgun.send_mail(
                email=[self.user_email],
                subject=f"Notification for {self.name}",
                text=f"Your alert {self.name} has reached a price under {self.price_limit}. The latest price is {self.item.price}. Go to this address to check your item: {self.item.url}.",
                html=f'<p>Your alert {self.name} has reached a price under {self.price_limit}.</p><p>The latest price is {self.item.price}. Check your item out <a href="{self.item.url}>here</a>.</p>',
            )



# Notes:
# If there is a superclass, the dataclass generated init method will call the init method of the superclass for you.
# Superclasses don't have to be data classes.
# Dataclasses are code generators that generates init methods, repr methods, comparisons and hashing.
#  __post_init__(self) - method runs after the init method and has access to self i.e self.item_id for example.
