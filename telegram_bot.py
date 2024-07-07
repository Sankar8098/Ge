import re
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

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
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Send /replace <caption>|<rules>|<keep_original> or /caption <caption> to process.')

# Command handler for /replace
def replace(update: Update, context: CallbackContext) -> None:
    try:
        message = ' '.join(context.args)
        parts = message.split('|')
        
        if len(parts) != 3:
            update.message.reply_text('Invalid format. Please use "/replace <caption>|<rules>|<keep_original>".')
            return

        caption, rules, keep_original = parts
        keep_original = keep_original.lower() == 'true'

        new_caption = customize_captions(caption, rules, keep_original)
        update.message.reply_text(new_caption)
    except Exception as e:
        update.message.reply_text(f"Error: {e}")

# Command handler for /caption
def caption(update: Update, context: CallbackContext) -> None:
    try:
        caption = ' '.join(context.args)
        update.message.reply_text(caption)
    except Exception as e:
        update.message.reply_text(f"Error: {e}")

def main() -> None:
    # Replace 'YOUR_TOKEN_HERE' with your actual bot token
    updater = Updater("YOUR_TOKEN_HERE", use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("replace", replace))
    dispatcher.add_handler(CommandHandler("caption", caption))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
