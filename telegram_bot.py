import re
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

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
    await update.message.reply_text('Send /replacefilename <filename>|<rules> or /replacecaption <caption>|<rules> to process.')

# Command handler for /replacefilename
async def replace_filename(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        message = ' '.join(context.args)
        parts = message.split('|')
        
        if len(parts) != 2:
            await update.message.reply_text('Invalid format. Please use "/replacefilename <filename>|<rules>".')
            return

        filename, rules = parts
        new_filename = customize_text(filename, rules)
        await update.message.reply_text(new_filename)
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

# Command handler for /replacecaption
async def replace_caption(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        message = ' '.join(context.args)
        parts = message.split('|')
        
        if len(parts) != 2:
            await update.message.reply_text('Invalid format. Please use "/replacecaption <caption>|<rules>".')
            return

        caption, rules = parts
        new_caption = customize_text(caption, rules)
        await update.message.reply_text(new_caption)
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

def main() -> None:
    # Replace 'YOUR_TOKEN_HERE' with your actual bot token
    application = ApplicationBuilder().token("6769849216:AAEkJSTlvjgfaMOrpWFZ0WArvs9ERXL3Y4Y").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("replacefilename", replace_filename))
    application.add_handler(CommandHandler("replacecaption", replace_caption))

    application.run_polling()

if __name__ == '__main__':
    main()
