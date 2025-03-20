from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from core.main import TGGroup, TGInterface


async def handle_tournament_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    command_type: str,
) -> None:
    tg_chat_id: str = str(update.message.chat.id)
    chat_type: str = update.message.chat.type

    if chat_type != "supergroup":
        await update.message.reply_text(
            "Извините, данная команда доступна только в групповом чате ;((( "
        )
        return

    tg_group = TGGroup(id=tg_chat_id)
    tg_interface = TGInterface(tg_group)

    if command_type == "new":
        # новый турнир
        result = tg_interface.new_tournament(context.args)
    elif command_type == "stop":
        # остановить текущий турнир
        result = tg_interface.stop_tournament()
    elif command_type == "start":
        # стартуем турнир
        result = tg_interface.start_tournament()
    elif command_type == "price":
        # цена турнира
        result = tg_interface.add_price_tournament(context.args)
    elif command_type == "percent":
        # TODO подумать над тем как заводить
        # указываем процентное соотношение победителей
        result = tg_interface.add_percent_tournament(context.args)
    elif command_type == "add":
        # вход пользователя в турнир
        result = tg_interface.add_user(context.args)
    elif command_type == "entry":
        # докуп пользователя
        result = tg_interface.entry_user(context.args)
    elif command_type == "lose":
        # проигрыш пользователя
        result = tg_interface.lose_user(context.args)
    elif command_type == "status":
        # текущее состояние турнира
        result = tg_interface.status_tournament(context.args)
    elif command_type == "winners":
        # указываем победителей
        result = tg_interface.winners_users(context.args)
    else:
        result = "Неизвестная команда"

    await update.message.reply_text(result)


async def new_tournament(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await handle_tournament_command(update, context, "new")


async def stop_tournament(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await handle_tournament_command(update, context, "stop")


async def start_tournament(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await handle_tournament_command(update, context, "start")


async def add_price_tournament(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    await handle_tournament_command(update, context, "price")


def main_func(bot_token: str):
    app = ApplicationBuilder().token(bot_token).build()
    app.add_handler(CommandHandler("new", new_tournament))
    app.add_handler(CommandHandler("stop", stop_tournament))
    app.add_handler(CommandHandler("start", start_tournament))
    app.add_handler(CommandHandler("price", add_price_tournament))
    app.run_polling()


if __name__ == "__main__":
    from help.settings import BOT_TOKEN

    main_func(BOT_TOKEN)
