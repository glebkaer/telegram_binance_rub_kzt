from telegram.ext import Updater, CommandHandler, CallbackContext,\
    ConversationHandler, MessageHandler, Filters
from telegram import Update, ParseMode
from binance_api import get_simple_output_values_for_bot, get_complex_output_values_for_bot


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет, трейдер!")


def simple_rate(update: Update, context: CallbackContext):
    text = get_simple_output_values_for_bot()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


# def get_amount(update: Update, context: CallbackContext):
#     context.bot.send_message(chat_id=update.effective_chat.id, text='Please enter the sum in RUB\nBy default 10000')
#     return EXPECT_AMOUNT


def complex_rate(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Please w8, it takes time')
    try:
        amount = int(context.args[0])
    except (IndexError, ValueError):
        context.bot.send_message(chat_id=update.effective_chat.id, text='No value entered. By default 10000 RUB')
        amount = 10000
    text = get_complex_output_values_for_bot(amount)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    return ConversationHandler.END


# def amount_input_by_user(update: Update, context: CallbackContext):
#     try:
#         amount = int(update.message.text)
#     except ValueError:
#         update.message.reply_text('Not an integer')
#         return EXPECT_INFO
#     print(amount)
#     return EXPECT_INFO


def cancel(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Amount input cancelled by user. Send /complex_rate to start again')
    return ConversationHandler.END


def TelegramBot( token):
    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    simple_rate_handler = CommandHandler('simple_rate', simple_rate)
    complex_rate_handler = CommandHandler('complex_rate', complex_rate)
    # complex_rate_handler = ConversationHandler(
    #     entry_points=[CommandHandler('complex_rate', get_amount)],
    #     states={
    #         EXPECT_AMOUNT: [MessageHandler(Filters.text, amount_input_by_user)],
    #         EXPECT_INFO: [CommandHandler('get_value', complex_rate)]
    #     },
    #     fallbacks=[CommandHandler('cancel', cancel)])
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(simple_rate_handler)
    dispatcher.add_handler(complex_rate_handler)
    updater.start_polling()
    updater.idle()

