from db.main import DBAPI
from db.utils import TGGroup


class TGInterface:

    def __init__(self, tg_chat: TGGroup):
        # Создаем подключение к БД
        self.db_api = DBAPI(tg_chat)

    def new_tournament(self, args: list[str]) -> str:
        # проверим, есть ли в чате активные турниры
        if self.db_api.is_active_tournament is not None:
            text = (
                "Перед созданием нового турнира, Вам необходимо "
                + "завершить текущий. Команда для завершения активного "
                + "турнира: /stop "
            )
        else:
            if not args:
                text = (
                    "Необходимо задать название турнира,"
                    + " например: \n/new Новогодний турнир 2025"
                )
            else:
                tournament_name: str = " ".join(args)
                # Отправляем запрос на создание в БД
                db_response = self.db_api.make_tournment(tournament_name)
                if db_response.status == "error":
                    text = f"Ошибка создания турнира: {db_response.text}"
                else:
                    text = f"Турнир {tournament_name} успешно создан! Ждем игроков"
        return text
