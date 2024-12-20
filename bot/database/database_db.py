from tortoise import Tortoise


async def init_db():
    await Tortoise.init(
        db_url="sqlite://Database.db",
        modules={"models": ["models"]}
    )
    await Tortoise.generate_schemas()