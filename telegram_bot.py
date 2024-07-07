import re
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Function to customize captions
def customize_captions(caption, rules, keep_original=False):
    if keep_original:
        return caption

    # Split the rules by '|'
    transformations = rules.split('|')

    for transformation in transformations:
        if ':' in transformation:
            find, change = transformation.split(':', 1)
            # Create a regex pattern to match the whole word, case insensitive
            pattern = re.compile(r'\b' + re.escape(find) + r'\b', re.IGNORECASE)
            # Replace 'find' with 'change' in the caption
            caption = pattern.sub(change, caption)

    return caption

# Command handler for /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Send /replace <caption>|<rules>|<keep_original> or /caption <caption> to process.')

# Command handler for /replace
async def replace(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        message = ' '.join(context.args)
        parts = message.split('|')
        
        if len(parts) != 3:
            await update.message.reply_text('Invalid format. Please use "/replace <caption>|<rules>|<keep_original>".')
            return

        caption, rules, keep_original = parts
        keep_original = keep_original.lower() == 'true'

        new_caption = customize_captions(caption, rules, keep_original)
        await update.message.reply_text(new_caption)
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

# Command handler for /caption
async def caption(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        caption = ' '.join(context.args)
        await update.message.reply_text(caption)
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

def main() -> None:
    # Replace 'YOUR_TOKEN_HERE' with your actual bot token
    application = ApplicationBuilder().token("6769849216:AAEkJSTlvjgfaMOrpWFZ0WArvs9ERXL3Y4Y").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("replace", replace))
    application.add_handler(CommandHandler("caption", caption))

    application.run_polling()

if __name__ == '__main__':
    main()
