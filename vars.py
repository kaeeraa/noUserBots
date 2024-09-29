from typing import Dict
from loguru import logger
from sys import stdout
from dotenv import dotenv_values
from hikari import Intents, GatewayBot
from arc import GatewayClient

logger.remove()
logger.add(sink=stdout,
           format="<level>{time:HH:mm:ss.SSS}</level> | <level>{level.icon}</level> | <level>{message}</level>")

logger.level(name="INFO", color="<green>")
logger.level(name="ERROR", color="<red>")


env: Dict[str, str | None] = dotenv_values(dotenv_path=".env", verbose=True)

bot = GatewayBot(
    token=env["BOT_TOKEN"],
    intents=Intents.ALL
)

client = GatewayClient(bot)
