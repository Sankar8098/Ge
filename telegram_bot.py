import re
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Function to customize text based on find:replace pairs
def customize_text(text, rules):
    transformations = rules.split('|')

    for transformation in transformations:
        if ':' in transformation:
            find, change = transformation.split(':', 1)
            # Create a regex pattern to match the whole word, case insensitive
            pattern = re.compile(r'\b' + re.escape(find) + r'\b', re.IGNORECASE)
            # Replace 'find' with 'change' in the text
            text = pattern.sub(change, text)
        else:
            # Remove the word if no replacement is specified
            pattern = re.compile(r'\b' + re.escape(transformation) + r'\b', re.IGNORECASE)
            text = pattern.sub('', text)

    return text

# Command handler for /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Send /replacecaption <rules> to process captions of videos.')

# Command handler for /replacecaption
async def replace_caption_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        if len(context.args) != 1:
            await update.message.reply_text('Invalid format. Please use "/replacecaption <rules>".')
            return

        rules = context.args[0]
        context.user_data['rules'] = rules
        await update.message.reply_text('Rules set! Now send a video with a caption to modify.')
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

# Handler for video messages
async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        rules = context.user_data.get('rules')
        if not rules:
            await update.message.reply_text('Please set the rules first using /replacecaption <rules>.')
            return

        if update.message.video:
            caption = update.message.caption or ''
            new_caption = customize_text(caption, rules)

            video_file = await update.message.video.get_file()
            file_path = f"/tmp/{video_file.file_unique_id}.mp4"
            await video_file.download_to_drive(file_path)

            await context.bot.send_video(
                chat_id=update.message.chat_id,
                video=open(file_path, 'rb'),
                caption=new_caption
            )

            os.remove(file_path)
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

def main() -> None:
    # Replace 'YOUR_TOKEN_HERE' with your actual bot token
    application = ApplicationBuilder().token("YOUR_TOKEN_HERE").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("replacecaption", replace_caption_command))
    application.add_handler(MessageHandler(filters.VIDEO, handle_video))

    application.run_polling()

if __name__ == '__main__':
    main()
