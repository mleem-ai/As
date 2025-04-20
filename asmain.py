import telebot
import os
from dotenv import load_dotenv

# Load configuration
load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ADMIN_ID = os.getenv('ADMIN_CHAT_ID')

# Validate configuration
if not TOKEN:
    raise ValueError("Telegram bot token not found in environment variables")
if not ADMIN_ID:
    raise ValueError("Admin chat ID not found in environment variables")

# Create bot instance
bot = telebot.TeleBot(TOKEN)

# Bot texts - Warm English Version
TEXTS = {
    "welcome": """✨ *Welcome to the Engine of Progress!* ✨  

Let's get to know each other better! Answer these 5 quick questions so we can help you effectively:  

1. **🛠 What do you do?**  
   (Tell us about your work, projects, or passions—what excites you?)  

2. **🎯 Why are you here?**  
   (What would you like to achieve? What help or advice are you looking for?)  

3. **📈 Where are you growing next?**  
   (What skills are you sharpening? Any big professional dreams?)  

4. **🌱 What's your current life chapter?**  
   (E.g., *"Launching a startup," "Career switch," "Exploring new horizons"*)  

5. **✏️ What's your name?**  
   (What should we call you?)  

Reply with numbered answers (1.-5.). Let's go! 🚀""",

    "response": """📬 *Thank you!* We've received your answers and will review them shortly.  

Expect a reply soon—make sure your DMs are open! 💌""",

    "error": "⚠️ Oops! Something went wrong. Please try again or contact support.",

    "invalid_format": """❌ *Please use this format:*  

1. [Your work/passion]  
2. [Your goal]  
3. [Skills you're developing]  
4. [Current life phase]  
5. [Your name]  

Example:  
1. UX Designer & coffee enthusiast  
2. Need advice on freelancing  
3. Learning advanced prototyping  
4. Building my solo business  
5. Alex""",

    "received_application": """📋 *New Application*  
──────  
**User ID:** `{user_id}`  
**Username:** @{username}  
**Name:** {full_name}  

**Responses:**  
{answers}  
──────  
✨ Forwarded to the team."""
}

# Start command handler
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, TEXTS["welcome"], parse_mode='Markdown')
    bot.register_next_step_handler(message, process_answers)

# Process user answers
def process_answers(message):
    try:
        # Validate the message contains all 5 answers
        if not all(f"{i}." in message.text for i in range(1, 6)):
            bot.send_message(message.chat.id, TEXTS["invalid_format"], parse_mode='Markdown')
            bot.register_next_step_handler(message, process_answers)
            return

        # Prepare user info
        user_id = message.from_user.id
        username = message.from_user.username if message.from_user.username else "no_username"
        first_name = message.from_user.first_name or ""
        last_name = message.from_user.last_name or ""
        full_name = f"{first_name} {last_name}".strip()

        # Format the message for admin
        admin_message = TEXTS["received_application"].format(
            user_id=user_id,
            username=username,
            full_name=full_name,
            answers=message.text
        )

        # Send to admin
        bot.send_message(ADMIN_ID, admin_message, parse_mode='Markdown')
        
        # Send confirmation to user
        bot.send_message(message.chat.id, TEXTS["response"], parse_mode='Markdown')

    except Exception as e:
        print(f"Error: {e}")
        bot.send_message(message.chat.id, TEXTS["error"])

# Start the bot
if __name__ == '__main__':
    print("Bot is running...")
    try:
        bot.infinity_polling()
    except Exception as e:
        print(f"Bot crashed with error: {e}")