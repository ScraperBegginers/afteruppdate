import aiofiles
from aiogram.types import FSInputFile


async def read_photo(name_photo: str):
    async with aiofiles.open(f'bot/photos/{name_photo}.jpg', 'rb') as photo:
        return FSInputFile(photo.name)