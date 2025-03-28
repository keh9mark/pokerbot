from db.core import DBCore
from db.utils import TGGroup
from db.db_api import db_session

from db.db_classes import Tournament

tg_chat = TGGroup(id="id123", name="гр1")

with db_session() as session:

    items = session.query(Tournament).all()
    db_api = DBCore(tg_chat, session)

    print(db_api.is_active_tournament)

    print(db_api.stop_tournament())

    # print(db_api.is_active_tournament)

    # print(db_api.make_tournment("turnir23"))

    # print(db_api.is_active_tournament)
