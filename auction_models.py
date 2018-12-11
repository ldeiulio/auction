import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import func
from sqlalchemy import and_

Base = declarative_base()


# Class that maps AuctionUser objects to records of table auction_user
# id is the primary key for record in database, created at time of commit, is integer
# username is stored as as string
# password stored as string, not encrypted in this implementation
# items establishes one to many relationship with Items
# bids establishes one to many relationship with Bids
class AuctionUser(Base):
    __tablename__ = 'auction_user'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)

    items = relationship("Items")
    bids = relationship("Bid")

    def __init__(self, username, password):
        self.username = username
        self.password = password

    # allows user to create on auction for item
    def auction_item(self, item_name, description):
        return Items(item_name, description, self.id)

    # allows user to create bid for specified item
    def bid_item(self, price, item):
        return Bid(price, self.id, item.id)


# Class that maps its Item objects to records of table items
# id is the primary key for record in database, created at time of commit, is integer
# description is details of item, is string
# start_time is time when auction for item was created, automatically specified
# user_id is id of user that created item auction, is Foreign key to AuctionUser
# user establishes many to one relationship to AuctionUser
# bids establishes one to many relationship to Bid
class Items(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    start_time = Column(DateTime, default=datetime.datetime.utcnow())
    user_id = Column(Integer, ForeignKey("auction_user.id"), nullable=False)

    user = relationship("AuctionUser", back_populates="items")
    bids = relationship("Bid", back_populates="item")

    def __init__(self, name, description, user_id):
        self.name = name
        self.description = description
        self.user_id = user_id

    # returns Bid with highest price value for item
    def highest_bid(self, session):
        max_bid = session.query(func.max(Bid.price)).filter(Bid.item_id == self.id).first()[0]
        return session.query(Bid).filter(and_(Bid.item_id == self.id, Bid.price == max_bid)).first()


# Class that maps its Bid objects to records of table bid
# id is the primary key for record in database, created at time of commit, is integer
# price is amount being used for bid on item, is float
# user_id is id of user that created Bid, is Foreign key to AuctionUser
# item_id is id of item being bid on, is Foreign key to Items
# user establishes many to one relationship to AuctionUser
# item establishes many to one relationship to Items
class Bid(Base):
    __tablename__ = 'bid'
    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey("auction_user.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)

    user = relationship("AuctionUser", back_populates="bids")
    item = relationship("Items", back_populates="bids")

    def __init__(self, price, user_id, item_id):
        self.price = price
        self.user_id = user_id
        self.item_id = item_id
