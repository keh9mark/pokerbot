from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from core.main import TGGroup, TGInterface


async def new_tournament(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    tg_chat_id: str = str(update.message.chat.id)
    chat_type: str = update.message.chat.type

    if chat_type != "supergroup":
        await update.message.reply_text(
            f"Извините, данная команда доступна только в групповом чате ;((( "
        )
    else:
        members = []
        tg_group = TGGroup(id=tg_chat_id)
        tg_intarface = TGInterface(tg_group)
        result = tg_intarface.new_tournament(context.args)
        await update.message.reply_text(result)


def main_func(bot_token: str):
    app = ApplicationBuilder().token(bot_token).build()
    app.add_handler(CommandHandler("new", new_tournament))
    app.run_polling()


if __name__ == "__main__":
    from help.settings import BOT_TOKEN

    main_func(BOT_TOKEN)
