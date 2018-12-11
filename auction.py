from auction_models import AuctionUser, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def main():
    engine = engine_creation()
    Base.metadata.create_all(engine)
    session = session_creation(engine)

    users = auction_user_creation()
    session_add_and_commit(session, users)

    baseball = auction_baseball_and_bid(users, session)

    query_highest_bid(baseball, session)


# creates engine to connect to database
def engine_creation():
    return create_engine('postgresql+pg8000://test:pass@localhost:5432/auction')


# creates session to communicate to database
def session_creation(engine):
    Session = sessionmaker(bind=engine)
    return Session()


# creates 3 users in database
def auction_user_creation():
    users = [AuctionUser("Bob", "password"), AuctionUser("John", "12345"),
             AuctionUser("Dave", "foobar")]
    print("creating users %s, %s, and %s\n" % (users[0].username, users[1].username, users[2].username))
    return users


# adds all users supplied and commits them to database
def session_add_and_commit(session, users):
    session.add_all(users)
    session.commit()


# creates an auction for a baseball by user 0 in list and bids for baseball by users 1 and 2 in list
def auction_baseball_and_bid(users, session):
    baseball = user_auctions_item(users[0], session)
    user_bids_on_item(users[1], baseball, 40, session)
    user_bids_on_item(users[2], baseball, 30, session)
    print()
    return baseball


#  has user create auction for item
def user_auctions_item(user, session):
    item = user.auction_item("baseball", "small hard ball to be hit with a bat")
    print("%s now auctioning %s\n" % (user.username, item.name))
    session.add(item)
    session.commit()
    return item


# has user make bid for item at specified price
def user_bids_on_item(user, item, price, session):
    bid = user.bid_item(price, item)
    print("%s now bidding on %s for $%.2f" % (user.username, item.name, bid.price))
    session.add(bid)
    session.commit()
    return bid


# wrapper for item.highest_bid with print statements
def query_highest_bid(item, session):
    print("Querying highest bidder for %s\n" % item.name)
    highest_bid = item.highest_bid(session)
    print("highest bidder for %s was %s for $%.2f" % (highest_bid.item.name, highest_bid.user.username, highest_bid.price))


# if current file is used as main file, start program by calling main()
if __name__ == "__main__":
    main()
