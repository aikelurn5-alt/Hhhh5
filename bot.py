import asyncio
import json
import os
import re
from urllib.parse import urlparse
from telebot.async_telebot import AsyncTeleBot
from keyboard import main_menu_keyboard, callback_handler
from address import get_address
from url import check_url
from stripe1 import stripe_1d
from rate import (
    is_rate_limited, 
    is_valid_url, 
    save_users, 
    is_registered, 
    get_role, 
    set_role, 
    register_user, 
    load_users, 
    has_permission, 
)
from proxy import check_proxy
from b3 import b3_auth


BOT_TOKEN = os.getenv("BOT_TOKEN", "8053442928:AAFJP6H7b85-5wdUck2O_L7hQ2DM_ewOtp4")
bot = AsyncTeleBot(BOT_TOKEN)

# Command to handle start
@bot.message_handler(commands=['start'])
async def send_welcome(message):
    user_id = message.from_user.id
    if not is_registered(user_id):
        await bot.reply_to(message, "You need to register first. Send `/register` to register.")
    else:
        # Send welcome message without the problematic image
        await bot.send_message(
            message.chat.id,
            (
                f"<u>〨〨〨〨[Welcome]〨〨〨〨</u>\n\n"
                f"Hello, <a href='tg://user?id={user_id}'>{message.from_user.first_name}</a>! Welcome from <b>Hyeri Area.</b>\n\n"
                "<u>Bot Admins</u>\n"
                "@Nico3x\n\n"
                "<i>☇ I am a simple bot for helping people.\n"
                "☇ Type /cmds to check all my commands.</i>\n"
                "<b>If there are any errors, please inform the Admins.</b>\n"
            ),
            reply_markup=main_menu_keyboard(),
            parse_mode="HTML"
        )

# Alternative: Use a local image or Telegram file_id instead of URL
async def send_welcome_with_image(message):
    user_id = message.from_user.id
    if not is_registered(user_id):
        await bot.reply_to(message, "You need to register first. Send `/register` to register.")
    else:
        try:
            # Try to send the image first
            await bot.send_photo(
                message.chat.id,
                "https://t.me/ysigsbssosb/2",  # Problematic URL
                caption=(
                    f"<u>〨〨〨〨[Welcome]〨〨〨〨</u>\n\n"
                    f"Hello, <a href='tg://user?id={user_id}'>{message.from_user.first_name}</a>! Welcome from <b>Hyeri Area.</b>"
                ),
                parse_mode="HTML"
            )
        except Exception as e:
            # If image fails, send text only
            print(f"Image error: {e}")
            await send_welcome(message)

# Command to handle registration
@bot.message_handler(commands=['register'])
async def handle_register(message):
    user_id = message.from_user.id
    if is_registered(user_id):
        await bot.reply_to(message, "You are already registered!")
    else:
        register_user(user_id)
        await bot.reply_to(message, "You have been successfully registered!")

# Command to set roles
@bot.message_handler(commands=['setrole'])
async def set_user_role(message):
    if not has_permission(message.from_user.id, "owner"):
        await bot.reply_to(message, "You do not have permission to use this command.")
        return

    parts = message.text.split()
    if len(parts) < 3:
        await bot.reply_to(message, "Usage: /setrole {user_id} {role}")
        return

    try:
        target_user_id = int(parts[1])
    except ValueError:
        await bot.reply_to(message, "User ID must be a number.")
        return
        
    new_role = parts[2].lower()
    if new_role not in ['admin', 'owner', 'premium', 'free']:
        await bot.reply_to(message, "Invalid role! Available roles: admin, owner, premium, free.")
        return

    set_role(target_user_id, new_role)
    await bot.reply_to(message, f"User {target_user_id} has been assigned the role {new_role}.")

# Command to check user role
@bot.message_handler(commands=['role'])
async def check_user_role(message):
    user_id = message.from_user.id
    if not is_registered(user_id):
        await bot.reply_to(message, "You must register first by sending `/register`.")
        return

    role = get_role(user_id)
    await bot.reply_to(message, f"Your current role is: {role}")

# Command to get address
@bot.message_handler(commands=['address'])
async def send_address(message):
    user_id = message.from_user.id
    if not is_registered(user_id):
        await bot.reply_to(message, "You must register first by sending `/register`.")
        return

    country_code = message.text[len('/address '):].strip()
    if country_code:
        try:
            address = get_address(country_code)
            await bot.reply_to(message, address, parse_mode="Markdown")
        except Exception as e:
            await bot.reply_to(message, f"Error: {e}")
    else:
        await bot.reply_to(message, "Usage: /address {country_code}")

# Command to check URL
@bot.message_handler(commands=['url'])
async def send_url(message):
    user_id = message.from_user.id
    if not is_registered(user_id):
        await bot.reply_to(message, "You must register first by sending `/register`.")
        return

    url = message.text[len('/url '):].strip()
    if not re.match(r'^https?://[^\s]+$', url):
        await bot.reply_to(message, "Invalid URL format.")
        return

    bot0 = await bot.reply_to(message, "Please wait... ⏳")
    try:
        result = await check_url(url)
        await bot.edit_message_text(result, chat_id=bot0.chat.id, message_id=bot0.message_id)
    except Exception as e:
        await bot.edit_message_text(f"Error: {e}", chat_id=bot0.chat.id, message_id=bot0.message_id)

# Command to check stripe
@bot.message_handler(commands=['chk'])
async def send_stripe(message):
    user_id = message.from_user.id
    if not has_permission(user_id, "premium"):
        await bot.reply_to(message, "You do not have permission to use this command. Only Premium or Owner roles can access this feature.")
        return
    if not is_registered(user_id):
        await bot.reply_to(message, "You must register first by sending `/register`.")
        return
    if is_rate_limited(user_id):
        await bot.reply_to(message, "You are sending messages too fast. Please slow down.")
        return
    bot0 = await bot.reply_to(message, "Checking your card...")
    card_details = message.text[len('/chk '):].strip()
    if card_details:
        try:
            result = await stripe_1d(card_details)
            await bot.edit_message_text(result, chat_id=bot0.chat.id, message_id=bot0.message_id)
        except Exception as e:
            await bot.edit_message_text(f"Error: {e}", chat_id=bot0.chat.id, message_id=bot0.message_id)
    else:
        await bot.edit_message_text("Usage: /chk {card_details}", chat_id=bot0.chat.id, message_id=bot0.message_id)

@bot.message_handler(commands=['bb'])
async def send_b3(message):
    user_id = message.from_user.id
    if not has_permission(user_id, "premium"):
        await bot.reply_to(message, "You do not have permission to use this command. Only Premium or Owner roles can access this feature.")
        return
    if not is_registered(user_id):
        await bot.reply_to(message, "You must register first by sending `/register`.")
        return
    if is_rate_limited(user_id):
        await bot.reply_to(message, "You are sending messages too fast. Please slow down.")
        return
    bot0 = await bot.reply_to(message, "Checking your card...")
    card_details = message.text[len('/bb '):].strip()
    if card_details:
        try:
            result = b3_auth(card_details)
            await bot.edit_message_text(result, chat_id=bot0.chat.id, message_id=bot0.message_id)
        except Exception as e:
            await bot.edit_message_text(f"Error: {e}", chat_id=bot0.chat.id, message_id=bot0.message_id)
    else:
        await bot.edit_message_text("Usage: /bb {card_details}", chat_id=bot0.chat.id, message_id=bot0.message_id)

# Echo command
@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    user_id = message.from_user.id
    if not is_registered(user_id):
        await bot.reply_to(message, "You must register first by sending `/register`.")
        return

    await bot.reply_to(message, f"`{message.text}`", parse_mode="Markdown")

# Main entry point to run the bot
async def main():
    print("Working Bot!!")
    await bot.polling()

if __name__ == "__main__":
    asyncio.run(main())            message.chat.id,
            "https://t.me/BruhNoValue/14",  # Image URL
            caption=(
                f"<u>〨〨〨〨[Welcome]〨〨〨〨</u>\n\n"
                f"Hello, <a href='tg://user?id={user_id}'>{message.from_user.first_name}</a>! Welcome from <b>Hyeri Area.</b>\n\n"
                "<u>Bot Admins</u>\n"
                "@Nico3x\n\n"
                "<i>☇ I am a simple bot for helping people.\n"
                "☇ Type /cmds to check all my commands.</i>\n"
                "<b>If there are any errors, please inform the Admins.</b>\n"
            ),
            reply_markup=main_menu_keyboard(),  # Inline Keyboard
            parse_mode="HTML"
        )

# Command to handle registration
@bot.message_handler(commands=['register'])
async def handle_register(message):
    user_id = message.from_user.id
    if is_registered(user_id):
        await bot.reply_to(message, "You are already registered!")
    else:
        register_user(user_id)
        await bot.reply_to(message, "You have been successfully registered!")

# Command to set roles
@bot.message_handler(commands=['setrole'])
async def set_user_role(message):
    if not has_permission(message.from_user.id, "owner"):
        await bot.reply_to(message, "You do not have permission to use this command.")
        return

    parts = message.text.split()
    if len(parts) < 3:
        await bot.reply_to(message, "Usage: /setrole {user_id} {role}")
        return

    target_user_id, new_role = parts[1], parts[2].lower()
    if new_role not in ['admin', 'owner', 'premium', 'free']:
        await bot.reply_to(message, "Invalid role! Available roles: admin, owner, premium, free.")
        return

    set_role(target_user_id, new_role)
    await bot.reply_to(message, f"User {target_user_id} has been assigned the role {new_role}.")

# Command to check user role
@bot.message_handler(commands=['role'])
async def check_user_role(message):
    user_id = message.from_user.id
    if not is_registered(user_id):
        await bot.reply_to(message, "You must register first by sending `/register`.")
        return

    role = get_role(user_id)
    await bot.reply_to(message, f"Your current role is: {role}")

# Command to get address
@bot.message_handler(commands=['address'])
async def send_address(message):
    user_id = message.from_user.id
    if not is_registered(user_id):
        await bot.reply_to(message, "You must register first by sending `/register`.")
        return

    country_code = message.text[len('/address '):].strip()
    if country_code:
        try:
            address = get_address(country_code)
            await bot.reply_to(message, address, parse_mode="Markdown")
        except Exception as e:
            await bot.reply_to(message, f"Error: {e}")
    else:
        await bot.reply_to(message, "Usage: /address {country_code}")

# Command to check URL
@bot.message_handler(commands=['url'])
async def send_url(message):
    user_id = message.from_user.id
    if not is_registered(user_id):
        await bot.reply_to(message, "You must register first by sending `/register`.")
        return

    url = message.text[len('/url '):].strip()
    if not re.match(r'^https?://[^\s]+$', url):
        await bot.reply_to(message, "Invalid URL format.")
        return

    bot0 = await bot.reply_to(message, "Please wait... ⏳")
    try:
        result = await check_url(url)
        await bot.edit_message_text(result, chat_id=bot0.chat.id, message_id=bot0.message_id)
    except Exception as e:
        await bot.edit_message_text(f"Error: {e}", chat_id=bot0.chat.id, message_id=bot0.message_id)

# Command to check stripe
@bot.message_handler(commands=['chk'])
async def send_stripe(message):
    user_id = message.from_user.id
    if not has_permission(user_id, "premium"):
        await bot.reply_to(message, "You do not have permission to use this command. Only Premium or Owner roles can access this feature.")
        return
    if not is_registered(user_id):
        await bot.reply_to(message, "You must register first by sending `/register`.")
        return
    if is_rate_limited(user_id):
        await bot.reply_to(message, "You are sending messages too fast. Please slow down.")
        return
    bot0 = await bot.reply_to(message, "Checking your card...")
    card_details = message.text[len('/chk '):].strip()
    if card_details:
        try:
            result = await stripe_1d(card_details)
            await bot.edit_message_text(result, chat_id=bot0.chat.id, message_id=bot0.message_id)
        except Exception as e:
            await bot.edit_message_text(f"Error: {e}", chat_id=bot0.chat.id, message_id=bot0.message_id)
    else:
        await bot.edit_message_text("Usage: /chk {card_details}", chat_id=bot0.chat.id, message_id=bot0.message_id)

@bot.message_handler(commands=['bb'])
async def send_stripe(message):
    user_id = message.from_user.id
    if not has_permission(user_id, "premium"):
        await bot.reply_to(message, "You do not have permission to use this command. Only Premium or Owner roles can access this feature.")
        return
    if not is_registered(user_id):
        await bot.reply_to(message, "You must register first by sending `/register`.")
        return
    if is_rate_limited(user_id):
        await bot.reply_to(message, "You are sending messages too fast. Please slow down.")
        return
    bot0 = await bot.reply_to(message, "Checking your card...")
    card_details = message.text[len('/bb'):].strip()
    if card_details:
        try:
            result = b3_auth(card_details)
            await bot.edit_message_text(result, chat_id=bot0.chat.id, message_id=bot0.message_id)
        except Exception as e:
            await bot.edit_message_text(f"Error: {e}", chat_id=bot0.chat.id, message_id=bot0.message_id)
    else:
        await bot.edit_message_text("Usage: /b3 {card_details}", chat_id=bot0.chat.id, message_id=bot0.message_id)
# Echo command
@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    user_id = message.from_user.id
    if not is_registered(user_id):
        await bot.reply_to(message, "You must register first by sending `/register`.")
        return

    await bot.reply_to(message, f"`{message.text}`", parse_mode="Markdown")

# Main entry point to run the bot
async def main():
    print("Working Bot!!")
    await bot.polling()

if __name__ == "__main__":
    asyncio.run(main())
