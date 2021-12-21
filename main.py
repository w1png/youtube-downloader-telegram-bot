from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InputFile

from youtube_dl import YoutubeDL
from os import remove, listdir

token = list(map(str.rstrip, open("token.txt").readlines()))[0]
bot = Bot(token=token)
dp = Dispatcher(bot)

ytdl_options = {
    "no_warnings": True,
    "quiet": True,
    "outtmpl": "videos/video",
    "noplaylist": True,
}

@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    await bot.send_message(
        chat_id=message.chat.id,
        text="Hello! Just send me the link to the Youtube video and I will send you the mp4 file of it.",
    )
    

@dp.message_handler()
async def main(message: types.Message):
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"Trying to download {message.text}",
        disable_web_page_preview=True
    )
    try:
        with YoutubeDL(ytdl_options) as ydl:
            video_url = message.text
            meta = ydl.extract_info(video_url, download=False)
            video_title = meta.get('title', None)
            if meta["duration"] < 300:
                if meta["duration"] >= 60:
                    await bot.send_message(
                        chat_id=message.chat.id,
                        text=f"Videos longer than a minute take a relatively long time to download.",
                    )
                
                for file in listdir("videos/"):
                    remove("videos/" + file)
                ydl.download([video_url])
                
                await bot.send_document(
                    chat_id=message.chat.id,
                    document=InputFile(path_or_bytesio="videos/" + listdir("videos/")[0])
                )
                await bot.send_message(
                    chat_id=message.chat.id,
                    text=f"\"{video_title}\" was downloaded!",
                )
            else:
                await bot.send_message(
                    chat_id=message.chat.id,
                    text=f"Videos longer than 5 minutes are not allowed!",
                )
    except:
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"An error occured :(",
        )
        
        
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
