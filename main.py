import os
from dotenv import load_dotenv
import random
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import ParseMode

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bull_level = [100, 500, 1500]
user_points = {}

def generate_user_list():
    card = [{"A":1},{"2":2},{"3":3},{"4":4},{"5":5},{"6":6},{"7":7},{"8":8},{"9":9},
        {"10":10},{"J":10},{"Q":10},{"K":10}]*4

    random.shuffle(card)
    USER = 10
    user_list = []
    for i in range(USER):
        user_list.append(card[0+5*i:5+5*i])
    
    return user_list

# 添加管理员控制机器人功能
def start(update: Update, context: CallbackContext):
    if update.message.from_user.id == ADMIN_ID:
        update.message.reply_text("欢迎使用管理员功能！")
    else:
        update.message.reply_text("您无权使用管理员功能！")

def stop(update: Update, context: CallbackContext):
    if update.message.from_user.id == ADMIN_ID:
        update.message.reply_text("机器人已静默！")
        updater.stop()
    else:
        update.message.reply_text("您无权使用管理员功能！")


# 添加管理员操作用户积分功能
def manage_points(update: Update, context: CallbackContext):
    if update.message.from_user.id == ADMIN_ID:
        text = update.message.text.split()
        user_id = update.message.reply_to_message.from_user.id
        if len(text) == 1 and text[0].startswith('+') and text[0][1:].isdigit():
            points = int(text[0][1:])
            user_points[user_id] = user_points.get(user_id, 0) + points
            context.bot.send_message(update.message.chat_id, f"用户的积分已经增加了 {points}，当前积分为 {user_points[user_id]}")
        elif len(text) == 1 and text[0].startswith('-') and text[0][1:].isdigit():
            points = int(text[0][1:])
            user_points[user_id] = user_points.get(user_id, 0) - points
            context.bot.send_message(update.message.chat_id, f"用户的积分已经减少了 {points}，当前积分为 {user_points[user_id]}")
        else:
            context.bot.send_message(update.message.chat_id, "请输入正确的操作指令，如：'+10' 或 '-5'")
    else:
        update.message.reply_text("您无权使用管理员功能！")

# 添加用户下注功能
# 添加用户下注功能
def place_bet(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    text = update.message.text.replace(" ", "")  # 去掉空格
    if text.startswith("X") and text[1:].isdigit():
        bet_amount = int(text[1:])
        if user_points.get(user_id, 0) >= bet_amount:
            user_points[user_id] -= bet_amount
            user_balance = user_points[user_id]
            mention = update.message.from_user.mention_html()
            context.bot.send_message(update.message.chat_id, f"👤{mention} \n成功下注 {bet_amount} \n余额还剩 {user_balance} ", parse_mode=ParseMode.HTML, reply_to_message_id=update.message.message_id)
        else:
            context.bot.send_message(update.message.chat_id, "积分不足，无法下注！", reply_to_message_id=update.message.message_id)

    else:
        context.bot.send_message(user_id, "请输入正确的下注指令，如：'X100'")





def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("stop", stop))
    dp.add_handler(MessageHandler(Filters.reply & Filters.text, manage_points))
    dp.add_handler(MessageHandler(Filters.text & Filters.regex(r'^X \d+$'), place_bet))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
