import openai

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

OPEN_AI_TOKEN = "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"
openai.api_key = OPEN_AI_TOKEN

BOT_TOKEN = "5991644111:AAE-XC7eTh84hY82lNwkC5bNNkbC6RcLi40"
bot = Bot(token=BOT_TOKEN)
dispatcher = Dispatcher(bot)


@dispatcher.message_handler(commands=["start"])
async def start_command(message):
    await message.reply(
        "Щоб отримати вірш, який містить вказані слова, введи їх через пробіл:"
    )


@dispatcher.message_handler(commands=["help"])
async def help_command(message):
    await message.reply(
        "Привіт! Я Bot, який приймає список слів та повертає вірш, який містить усі вказані слова. "
        "Всі вірші генеруються за допомогою OpenAI. Щоб спробувати, як працює цей бот, введи команду /start"
    )


@dispatcher.message_handler()
async def get_poem(message):
    user_input = message.text
    words = user_input.split()
    if len(words) > 20:
        await message.reply("Введено забагато слів, їх має бути не більше 20. Спробуй ще раз.")

    prompt = "Hi! Write a poem with rhyme and common sense using following words (note, " \
             "you should use all of them): " + ", ".join(words) + ". Write not more than 300 symbols. Write " \
                                                                  "in William Shakespeare style"

    try:
        response = openai.Completion.create(
            engine='gpt-3.5-turbo',
            prompt=prompt,
            max_tokens=600,
            temperature=0,
        )

        poem = response.choices[0].text.strip()
        await message.reply(poem)
    except Exception as e:
        await message.reply(f"Не вдається створити вірш з вказаними словами. Ось в чому проблема: {e}")


if __name__ == "__main__":
    executor.start_polling(dispatcher)
