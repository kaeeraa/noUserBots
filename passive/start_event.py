from vars import bot, logger
from hikari import StartedEvent
from hikari import Activity, ActivityType


async def on_ready(event: StartedEvent) -> None:
    logger.info(f"Am I alive? {bot.is_alive}")
    await bot.update_presence(activity=Activity(
        name="What's up, uB?", type=ActivityType.WATCHING))
