import traceback

from db.utils import get_datetime_msk, DBResponse, TGGroup, ActiveTournament
from db.db_classes import Chat, Tournament, User, UserGame


class DBCore:

    def __init__(self, tg_group: TGGroup, session):
        self.tg_group = tg_group
        self.session = session
        self.chat_item = self.get_chat_instance()

    def get_chat_instance(self):
        chat_instance = (
            self.session.query(Chat).filter(Chat.tg_id == self.tg_group.id).first()
        )
        if chat_instance is None:
            chat_instance = Chat(tg_id=self.tg_group.id, name=self.tg_group.name)
            self.session.add(chat_instance)
            self.session.commit()
        return chat_instance

    @property
    def is_active_tournament(self) -> ActiveTournament | None:
        info = None
        for tournament in self.chat_item.tournaments:
            if tournament.is_active:
                info = ActiveTournament(id=tournament.id, name=tournament.name)
                break
        return info

    @property
    def active_tournament(self) -> Tournament | None:
        for tournament in self.chat_item.tournaments:
            if tournament.is_active:
                return tournament

    @property
    def tournaments(self) -> dict:
        return {
            tournament.name: tournament for tournament in self.chat_item.tournaments
        }

    def make_tournment(self, tournament_name: str) -> DBResponse:
        if tournament_name in self.tournaments:
            return DBResponse(
                status="error",
                text="Турнир с таким названием уже был. "
                + " Придумайте новое название",
            )
        else:
            if self.is_active_tournament is not None:
                return DBResponse(
                    status="error",
                    text="Необходимо завершить текущий турнир",
                )
            tournament = Tournament(
                name=tournament_name,
                created_at=get_datetime_msk(),
                chat=self.chat_item,
            )
            self.session.add(tournament)
            self.session.commit()
            return DBResponse(status="success", text="")

    def stop_tournament(self) -> DBResponse:
        try:
            active_tournament = self.active_tournament
            if active_tournament is None:
                return DBResponse(
                    status="error",
                    text="Нет активных турниров",
                )
            active_tournament.is_active = False
            active_tournament.end_date = get_datetime_msk()
            self.session.add(active_tournament)
            self.session.commit()
            result = DBResponse(status="success", text="")
        except Exception:
            print(traceback.format_exc())
            result = DBResponse(
                status="error",
                text="Непревиденная ошибка. Обратитесь к разработчику",
            )
        return result

    def start_tournament(self) -> DBResponse:
        active_tournament = self.active_tournament
        if active_tournament.start_date is not None:
            result = DBResponse(
                status="error",
                text=f"Турнир {active_tournament.name} уже запущен",
            )
        try:
            active_tournament.start_date = get_datetime_msk()
            self.session.add(active_tournament)
            self.session.commit()
            result = DBResponse(status="success", text="")
        except Exception:
            print(traceback.format_exc())
            result = DBResponse(
                status="error",
                text="Непредвиденная ошибка. Обратитесь к разработчику",
            )
        return result

    def add_price_tournament(self, price: int) -> DBResponse:
        try:
            active_tournament = self.active_tournament
            active_tournament.price = price
            result = DBResponse(status="success", text="")
        except Exception:
            print(traceback.format_exc())
            result = DBResponse(
                status="error",
                text="Непредвиденная ошибка. Обратитесь к разработчику",
            )
        return result

    def _get_user_in_db(self, username: str) -> User:
        user_obj = self.session.query(User).filter(User.username == username).first()
        if user_obj is not None:
            print(f"Юзер @{username} есть в бд")
            return user_obj
        user_obj = User(username=username)
        print(f"Создали нового @{username}")
        self.session.add(user_obj)
        return user_obj

    def _set_usergame(self, user_obj: User) -> None:
        user_game = UserGame(
            user=user_obj,
            tournament=self.active_tournament,
            attached=get_datetime_msk(),
        )
        self.session.add(user_game)
        self.session.commit()

    def add_user(self, username: str) -> DBResponse:
        active_tournament = self.active_tournament
        user_games = active_tournament.user_games
        already_user_game = list(
            filter(lambda obj: obj.user.username == username, user_games)
        )
        if already_user_game:
            result = DBResponse(
                status="error",
                text=f"Пользователь @{username} уже участвует в турнире",
            )
        else:
            user_obj = self._get_user_in_db(username)
            self._set_usergame(user_obj)
            result = DBResponse(status="success", text="")
        return result

    def remove_user(self, username: str) -> DBResponse:
        active_tournament = self.active_tournament
        user_games = active_tournament.user_games
        already_user_games = list(
            filter(lambda obj: obj.user.username == username, user_games)
        )
        if not already_user_games:
            result = DBResponse(
                status="error",
                text=f"Пользователь @{username} не участвует в турнире",
            )
        else:
            self.session.delete(already_user_games[0])
            self.session.commit()
            result = DBResponse(status="success", text="")
        return result

    def rebay_user(self, username: str) -> DBResponse:
        active_tournament = self.active_tournament
        user_games = active_tournament.user_games
        already_user_games = list(
            filter(lambda obj: obj.user.username == username, user_games)
        )
        if not already_user_games:
            result = DBResponse(
                status="error",
                text=f"Пользователь @{username} не участвует в турнире",
            )
        else:
            user_game = already_user_games[0]
            user_game.rebuys += 1
            self.session.add(user_game)
            result = DBResponse(
                status="success", text=f"кол-во закупов: {user_game.rebuys}"
            )
        return result
