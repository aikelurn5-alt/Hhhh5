from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from telebot.async_telebot import AsyncTeleBot

# Function to create the main menu keyboard
def main_menu_keyboard():
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton("Owner", url="https://t.me/TrickLabGroup")
    button2 = InlineKeyboardButton("Group", url="https://t.me/TrickLabGroup")
    button3 = InlineKeyboardButton("Channel", url="https://t.me/TrickLab")

    
    # Add all buttons at once
    markup.add(button2, button3)
    markup.add(button1)
    return markup

# Function to create the admin keyboard
def admin_keyboard():
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton("Back to Main Menu", callback_data="back_to_main")
    markup.add(button1)
    return markup

# Callback function to handle all button presses
async def callback_handler(call, bot):
    if call.data == "opt1":  # User clicked "Admin"
        # Update the image and text
        admin_photo_url = "https://t.me/LisaLoverLayBruh/72"  # Replace with your admin image URL or file path
        admin_text = (
            "═══════[Admins]═══════\n\n"
            "*Admins:*\n"
            "@BruhNoCounter\n"
            "@Sachinhck\n\n"
            "_Feel free to reach out if you need any help._"
        )

        # Edit the photo and text
        media = InputMediaPhoto(media=admin_photo_url, caption=admin_text, parse_mode="Markdown")
        await bot.edit_message_media(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            media=media
        )

        # Send the admin keyboard
        admin_markup = admin_keyboard()
        await bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=admin_markup
        )
    
    elif call.data == "opt2":
        # Replace the media with a simple text message
        option2_text = "You selected *Option 2*.\nHere is the updated information without a photo."

        await bot.edit_message_caption(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            caption=option2_text,
            parse_mode="Markdown"
        )

    elif call.data == "back_to_main":
        # Go back to the main menu
        markup = main_menu_keyboard()
        await bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=markup
        )
    else:
        # Handle unknown actions
        await bot.answer_callback_query(call.id, "Unknown action!")
