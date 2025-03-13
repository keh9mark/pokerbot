import typing

from db.utils import get_datetime_msk, DBResponse, TGGroup


DATABASE = {}


class DBAPI:

    def __init__(self, tg_group: TGGroup):
        self.tg_group = tg_group
        self.chat_items = self.connect()

    @property
    def is_active_tournament(self) -> str | None:
        return self.chat_items["active"]

    @property
    def tournaments(self) -> dict:
        return self.chat_items["tournaments"]

    def connect(self) -> dict:
        if self.tg_group.id not in DATABASE:
            print("Создаем в БД сведения о новой группе")
            DATABASE[self.tg_group.id] = {"active": None, "tournaments": {}}
        return DATABASE[self.tg_group.id]

    def make_tournment(self, tournament_name: str) -> DBResponse:
        if tournament_name in self.tournaments:
            return DBResponse(
                status="error",
                text="Турнир с таким названием уже был. "
                + " Придумайте новое название",
            )
        else:
            self.tournaments[tournament_name] = {
                "id": id(self),
                "price": None,
                "name": tournament_name,
                "users": [],
                "counts": [],
                "rebuys": [],
                "times": {
                    "created": get_datetime_msk(),
                    "started": None,
                    "finished": None,
                },
            }
            self.chat_items["active"] = tournament_name
            return DBResponse(status="success", text="")
