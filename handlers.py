import random
from aiogram.types import Message
from aiogram.dispatcher.filters import Text
from bot_config import dp
import text
import game


@dp.message_handler(commands=['start'])
async def on_start(message: Message):
    await message.answer(text=f'{message.from_user.first_name}'
                              f'{text.greeting}')


@dp.message_handler(commands=['new_game'])
async def start_new_game(message: Message):
    game.new_game()
    if game.check_game():
        toss = random.choice([True, False])
        if toss:
            await player_turn(message)
        else:
            await bot_turn(message)

async def player_turn(message: Message):
    await message.answer(f'{message.from_user.first_name},'
                         f' твой ход! Сколько возьмешь конфет?')

@dp.message_handler()
async def take(message: Message):
    name = message.from_user.first_name
    if game.check_game:
        if message.text.isdigit():
            take = int(message.text)
            if (0 < take < 29) and take <= game.get_total():
                game.take_candies(take)
                if await check_win(message, take, 'player'):
                    return
                await message.answer(f'{name} взял {take} конфет и на столе осталось '
                                        f'{game.get_total()}. Ходит бот')
                await bot_turn(message)
            else:
                await message.answer('Что-то много берешь! Надо от 1 до 28')
        else:
            pass

async def bot_turn(message):
    total = game.get_total()
    if total <= 28:
        take = total
    else:
        take = random.randint(1,28)
    game.take_candies(take)
    await message.answer(f'Бот взял {take} конфет и их осталось {game.get_total()}')
    if await check_win(message, take, 'Бот'):
        return
    await player_turn(message)

async def check_win(message, take: int, player: str):
    if game.get_total() <= 0:
        if player == 'player':
            await message.answer(f'{message.from_user.first_name} и победил!')
        else:
            await message.answer(f'{message.from_user.first_name} ну как же так, БОТ взял {take} и победил!')
        game.new_game()
        return True
    else:
        return False
