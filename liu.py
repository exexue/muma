import logging,os,random
 
from telegram.ext import Updater, CommandHandler
from telegram.ext.dispatcher import run_async
from telegram.ext import MessageHandler, Filters
 
TOKEN = '1454306275:AAHbxYSgcGBoIY3t5k0BYTuyOQEU5YYn1Wo'
 
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
 
logger = logging.getLogger(__name__)
 
 




def start(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
 
 



def echo(update, context):
    if "rtmp" in update.message.text or "m3u8" in update.message.text:
        print("下载rtmp流")
        name = "/root/" + str(random.randint(100000,90000000)) + ".mp4"
        print(name)
        url = update.message.text.strip()
        print(url)
        cmd = "nohup ffmpeg -i '" + url + "' -c copy " + name + " && rclone copy " + name + " gdrive2:share/share/  && rm -rf " + name + "  >/dev/null 2>&1 &"
        os.system(cmd)
        
        context.bot.send_message(chat_id=update.effective_chat.id, text="执行小奶猫下载！") 
    else:

        context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

 
def main():
    updater = Updater(token=TOKEN, use_context=True)
 
    dp = updater.dispatcher
 
    dp.add_handler(CommandHandler("start", start))
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
 
    dp.add_handler(echo_handler)
    updater.start_polling()
    updater.idle()
 
 
if __name__ == '__main__':
    main()
