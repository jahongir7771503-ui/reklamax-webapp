from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class DesignState(StatesGroup):
    choose = State()
    file = State()
    colors = State()
    text = State()

async def start_design(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Menda tayyor dizayn bor")
    keyboard.add("Dizaynni siz qiling")

    await message.answer(
        "🎨 Dizayn bo‘yicha tanlang:",
        reply_markup=keyboard
    )
    await DesignState.choose.set()

async def choose_design(message: types.Message, state: FSMContext):
    await state.update_data(type=message.text)

    if message.text == "Menda tayyor dizayn bor":
        await message.answer("📎 Dizayn faylni yuboring")
        await DesignState.file.set()
    else:
        await message.answer("🎨 Ranglarni yozing")
        await DesignState.colors.set()

async def get_file(message: types.Message, state: FSMContext):
    await state.update_data(file=message.document.file_id)
    await message.answer("✅ Dizayn qabul qilindi")
    await state.finish()

async def get_colors(message: types.Message, state: FSMContext):
    await state.update_data(colors=message.text)
    await message.answer("✏️ Matnni yozing (nom, tel)")
    await DesignState.text.set()

async def get_text(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await message.answer("✅ Dizayn so‘rovi qabul qilindi")
    print(data)
    await state.finish()
