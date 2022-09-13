from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    CallbackContext, 
    MessageHandler, 
    Filters
)

user_data = dict()


STEP_ONE, STEP_TWO, STEP_THREE, STEP_FOUR = range(4)


def start(update: Update, context: CallbackContext) -> None:
    menu(update, context)


def menu(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Добрий настрый", callback_data="good_mood"),
            InlineKeyboardButton("Поганий настрый", callback_data="bad_mood"),
            InlineKeyboardButton("Я трохи прихворів", callback_data="illnes"),
            InlineKeyboardButton("Так в мене є плани", callback_data="plans"),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Який у вас сьогодні настрій ? Чи маєти ви якісь плани на сьогодні ?", reply_markup=reply_markup)


def bad_mood(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text="Після кожної бурі сонечко посміхається; для кожної проблеми є рішення, і невід’ємним обов’язком душі є бути в доброму дусі")

def good_mood(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text="Бажаю вам мати такий настрій кожен день!")

def illnes(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text="Сподіваюсь ви одужаєте якомого швидше.")


def user_name(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text="Як вас зовуть ? ")
    return STEP_TWO


def user_feeling(update, context):
    chat = update.effective_chat
    user_data['name'] = update.message.text 

    context.bot.send_message(chat_id=chat.id, text="Назвіть свої плани на сьогодні.")
    return STEP_THREE    


def user_answer(update, context):
    chat = update.effective_chat
    user_data['feeling'] = update.message.text 

    context.bot.send_message(chat_id=chat.id, text="Може у вас є плани на завтра ?Напишіть їх якщо є.")
    return STEP_FOUR    


def user_finish(update, context):
    chat = update.effective_chat
    user_data['answer'] = update.message.text

    user_text = "Спасибі за вашу увагу " + user_data.get('name') + " 😉"

    context.bot.send_message(chat_id=chat.id, text=user_text)
    return ConversationHandler.END  


def cancel(update, context):
    update.message.reply_text('Cancelled by user. Send /menu to start again')
    return ConversationHandler.END



def main() -> None:
    """Run the bot."""
    updater = Updater(token='5677184946:AAHKiPf_E9CyJwvVpX0aPaC_JlowHo04JjE')
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("menu", menu))
    dispatcher.add_handler(CallbackQueryHandler(bad_mood, pattern="bad_mood"))
    dispatcher.add_handler(CallbackQueryHandler(illnes, pattern="illnes"))
    dispatcher.add_handler(CallbackQueryHandler(good_mood, pattern="good_mood"))

    branch_user_handler = ConversationHandler(
        entry_points = [CallbackQueryHandler(user_name, 'plans')], 
        states={
            STEP_TWO:   [MessageHandler(Filters.text & (~ Filters.command), user_feeling)],
            STEP_THREE: [MessageHandler(Filters.text & (~ Filters.command), user_answer)],
            STEP_FOUR:  [MessageHandler(Filters.text & (~ Filters.command), user_finish)]
        }, 
        fallbacks=[CommandHandler("stop", cancel)]
    )

    dispatcher.add_handler(branch_user_handler)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()