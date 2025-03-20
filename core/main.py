import traceback

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

    def stop_tournament(self) -> str:
        active_tournament_name = self.db_api.is_active_tournament
        if not active_tournament_name:
            text = "Увы, нет активных турниров"
        else:
            db_response = self.db_api.stop_tournament()
            if db_response.status == "error":
                text = f"Ошибка остановки турнира: {db_response.text}"
            else:
                text = f"Турнир {active_tournament_name} успешно остановлен"
                # TODO вывести дополнительную статистику по турниру в текст
        return text

    def start_tournament(self) -> str:
        active_tournament_name = self.db_api.is_active_tournament
        if not active_tournament_name:
            text = "Увы, нет активных турниров"
        else:
            db_response = self.db_api.start_tournament()
            if db_response.status == "error":
                text = f"Ошибка запуска турнира: {db_response.text}"
            else:
                text = f"Турнир {active_tournament_name} успешно запущен"
                # TODO вывести дополнительную статистику по турниру в текст
        return text

    def add_price_tournament(self, args: list[str]) -> str:
        active_tournament_name = self.db_api.is_active_tournament
        if not active_tournament_name:
            text = "Увы, нет активных турниров"
        else:
            try:
                if len(args) != 1:
                    raise ArithmeticError("Некорректная сумма входа")
                price = int(args[0])
                db_response = self.db_api.add_price_tournament(price)
                if db_response.status == "error":
                    text = f"Ошибка установки суммы входа в турнир"
                else:
                    text = f"Сумма входа в турнир '{price} рублей' успешно установлена"
            except:
                print(traceback.format_exc())
                text = f"Ошибка установки суммы входа в турнир"
        return text
