import os
import yt_dlp
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Replace with your Bot Token from BotFather
TOKEN = '8029278006:AAE5NwFxZe4M8ZqdwtGbsOhXVD-k_VkXNfc'

# Create a function to handle /start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hi! Send me a YouTube video link, and I'll download it for you.")

# Create a function to download the video
def download_video(update: Update, context: CallbackContext):
    url = update.message.text  # Get the URL from the user's message
    chat_id = update.message.chat_id  # Get the chat ID

    # Check if the URL is a YouTube URL
    if "youtube.com" in url or "youtu.be" in url:
        # Set download options
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',  # Save as the video title
        }

        try:
            # Use yt-dlp to download the video
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                video_title = info_dict.get('title', None)
                file_path = f"downloads/{video_title}.mp4"

                # Send the video to the user
                if os.path.exists(file_path):
                    update.message.reply_video(video=open(file_path, 'rb'))
                    os.remove(file_path)  # Clean up by removing the downloaded video
        except Exception as e:
            update.message.reply_text(f"Error downloading video: {e}")
    else:
        update.message.reply_text("Please send a valid YouTube URL.")

# Main function to set up the bot
def main():
    # Set up the Updater and Dispatcher
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Register handlers for commands and messages
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, download_video))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
