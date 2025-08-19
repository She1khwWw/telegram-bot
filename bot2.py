from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
from datetime import datetime

API_TOKEN = "7837817367:AAFcUxRAk2a9g4_VT6A4BDIJCxTvuYEP1CM"
ADMIN_ID =  6197084874  # o'zingning Telegram ID'ingni yoz

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

def get_user_info(user: types.User) -> str:
    username = f"@{user.username}" if user.username else ""
    return f"{user.full_name} {username} (ID: {user.id})"

# /start komandasi
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("👋 Assalomu alaykum!\n\nIltimos, xabaringizni yuboring 😊")

# Ish vaqti tekshiruvchi funksiya
def is_work_time() -> tuple[bool, str]:
    now = datetime.now().time()
    start = datetime.strptime("09:00", "%H:%M").time()
    end = datetime.strptime("18:00", "%H:%M").time()

    if now < start:
        return False, "⏰ Ish vaqti hali boshlanmadi (9:00 dan keyin yozing)."
    elif now > end:
        return False, "⏰ Ish vaqti tugadi (ertaga 9:00 da yozing)."
    return True, ""

# Xabarlar uchun handler
@dp.message()
async def forward_message(message: types.Message):
    user_info = get_user_info(message.from_user)

    # Ish vaqti tekshirish
    ok, msg = is_work_time()
    if not ok:
        await message.answer(msg)
        return

    # Matn
    if message.text:
        await bot.send_message(ADMIN_ID, f"✉️ {user_info} yozdi:\n{message.text}")
        await message.answer("✅ Xabaringiz yuborildi.")

    # Ovozli xabar
    elif message.voice:
        await bot.send_voice(ADMIN_ID, message.voice.file_id,
                             caption=f"🎤 {user_info} ovozli xabar yubordi")
        await message.answer("🎤 Ovozli xabaringiz yuborildi.")

    # Video
    elif message.video:
        await bot.send_video(ADMIN_ID, message.video.file_id,
                             caption=f"🎬 {user_info} video yubordi")
        await message.answer("🎬 Videongiz yuborildi.")

    # Dumaloq video (VideoNote)
    elif message.video_note:
        await bot.send_video_note(ADMIN_ID, message.video_note.file_id)
        await bot.send_message(ADMIN_ID, f"🔵 {user_info} dumaloq video yubordi")
        await message.answer("🔵 Dumaloq videongiz yuborildi.")

    # Rasm
    elif message.photo:
        await bot.send_photo(ADMIN_ID, message.photo[-1].file_id,
                             caption=f"🖼 {user_info} rasm yubordi")
        await message.answer("🖼 Rasm yuborildi.")

    # Fayl
    elif message.document:
        await bot.send_document(ADMIN_ID, message.document.file_id,
                                caption=f"📂 {user_info} fayl yubordi")
        await message.answer("📂 Faylingiz yuborildi.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
