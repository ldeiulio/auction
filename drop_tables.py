from auction_models import AuctionUser, Items, Bid, Base
from sqlalchemy import create_engine

# Utility to quickly drop all tables, not strictly part of main project
# has no error handling, do not run twice in a row
if __name__ == '__main__':
    engine = create_engine('postgresql+pg8000://test:pass@localhost:5432/auction')
    Bid.__table__.drop(engine)
    Items.__table__.drop(engine)
    AuctionUser.__table__.drop(engine)
