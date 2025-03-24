import traceback

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
                "users": {},
                "counts": [],
                "times": {
                    "created": get_datetime_msk(),
                    "started": None,
                    "finished": None,
                },
            }
            self.chat_items["active"] = tournament_name
            return DBResponse(status="success", text="")

    def stop_tournament(self) -> DBResponse:
        try:
            active_tournament_name = self.chat_items["active"]
            self.chat_items["active"] = None
            self.tournaments[active_tournament_name]["times"][
                "finished"
            ] = get_datetime_msk()
            result = DBResponse(status="success", text="")
        except Exception:
            print(traceback.format_exc())
            result = DBResponse(
                status="error", text="Непредвиденная ошибка. Обратитесь к разработчику"
            )
        return result

    def start_tournament(self) -> DBResponse:
        active_tournament_name = self.chat_items["active"]
        if self.tournaments[active_tournament_name]["times"]["started"] is not None:
            result = DBResponse(
                status="error", text=f"Турнир {active_tournament_name} уже запущен"
            )
        try:
            self.tournaments[active_tournament_name]["times"][
                "started"
            ] = get_datetime_msk()
            result = DBResponse(status="success", text="")
        except Exception:
            print(traceback.format_exc())
            result = DBResponse(
                status="error", text="Непредвиденная ошибка. Обратитесь к разработчику"
            )
        return result

    def add_price_tournament(self, price: int) -> DBResponse:
        try:
            active_tournament_name = self.chat_items["active"]
            self.tournaments[active_tournament_name]["price"] = price
            result = DBResponse(status="success", text="")
        except Exception:
            print(traceback.format_exc())
            result = DBResponse(
                status="error", text="Непредвиденная ошибка. Обратитесь к разработчику"
            )
        return result

    def add_user(self, username: str) -> DBResponse:
        active_tournament_name = self.chat_items["active"]
        users = self.tournaments[active_tournament_name]["users"]
        if username in users:
            result = DBResponse(
                status="error", text=f"Пользователь @{username} уже участвует в турнире"
            )
        else:
            users[username] = {
                "start": get_datetime_msk(),
                "rebays": {},
                "finished": None,
            }
            result = DBResponse(status="success", text="")
        return result

    def remove_user(self, username: str) -> DBResponse:
        active_tournament_name = self.chat_items["active"]
        users = self.tournaments[active_tournament_name]["users"]
        if username not in users:
            result = DBResponse(
                status="error", text=f"Пользователь @{username} не участвует в турнире"
            )
        else:
            users.pop(username, None)
            result = DBResponse(status="success", text="")
        return result

    def rebay_user(self, username: str) -> DBResponse:
        active_tournament_name = self.chat_items["active"]
        users = self.tournaments[active_tournament_name]["users"]
        if username not in users:
            result = DBResponse(
                status="error", text=f"Пользователь @{username} не участвует в турнире"
            )
        else:
            rebays_count = len(users[username]["rebays"])
            users[username]["rebays"][rebays_count] = get_datetime_msk()
            result = DBResponse(
                status="success", text=f"кол-во закупов: {rebays_count}"
            )
        return result
