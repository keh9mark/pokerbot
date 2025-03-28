from db.core import DBCore
from db.utils import TGGroup
from db.db_api import db_session

from db.db_classes import Tournament

tg_chat = TGGroup(id="id123", name="гр1")

# with db_session() as session:

#     items = session.query(Tournament).all()
#     db_api = DBCore(tg_chat, session)

#     # print(db_api.is_active_tournament)

#     # print(db_api.stop_tournament())

#     # print(db_api.is_active_tournament)
#     # print(db_api.is_active_tournament)

#     # print(db_api.make_tournment("turnir251"))

#     # print(db_api.is_active_tournament)

#     # print(db_api.stop_tournament())

#     # print(db_api.is_active_tournament)
#     # print(db_api.add_price_tournament(234))
#     print("REM", db_api.remove_user("nick2"))
#     print()
#     print("ADD", db_api.add_user("nick2"))
#     print()
#     print("REM", db_api.remove_user("nick2"))
#     print()
#     print("ADD", db_api.add_user("nick2"))
#     print()
#     # print("REM", db_api.remove_user("nick2"))
#     # print()
#     # print("REM", db_api.remove_user("nick2"))
#     # print()
#     # print("REM", db_api.remove_user("nick2"))
#     # print()
#     # print("ADD", db_api.add_user("nick2"))
#     # print()
#     # print("REM", db_api.remove_user("nick2"))
#     # print()
#     # print("REM", db_api.remove_user("nick2"))

# with db_session() as session:

#     items = session.query(Tournament).all()
#     db_api = DBCore(tg_chat, session)
#     print("REM", db_api.remove_user("nick2"))
#     print()

# with db_session() as session:

#     items = session.query(Tournament).all()
#     db_api = DBCore(tg_chat, session)

#     print("ADD", db_api.add_user("nick2"))
#     print()

# with db_session() as session:

#     items = session.query(Tournament).all()
#     db_api = DBCore(tg_chat, session)
#     print("REM", db_api.remove_user("nick2"))
#     print()

# with db_session() as session:

#     items = session.query(Tournament).all()
#     db_api = DBCore(tg_chat, session)
#     print("ADD", db_api.add_user("nick2"))
#     print()

with db_session() as session:

    items = session.query(Tournament).all()
    db_api = DBCore(tg_chat, session)
    print("rebay", db_api.rebay_user("nick2"))
    print()
