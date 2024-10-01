from typing import Dict
from loguru import logger
from sys import stdout
from dotenv import dotenv_values
from hikari import Intents, GatewayBot
from arc import GatewayClient

logger.remove()
logger.add(sink=stdout,
           format="<level>{level.icon}</level> | <level>{time:HH:mm:ss.SSS}</level> | <level>{message}</level>")

logger.level(name="INFO", color="<green>", icon="I")
logger.level(name="ERROR", color="<red>", icon="E")


env: Dict[str, str | None] = dotenv_values(dotenv_path=".env", verbose=True)

if not env["BOT_TOKEN"]:
    logger.error("BOT_TOKEN not set")
    exit(code=1)

bot = GatewayBot(
    token=env["BOT_TOKEN"],
    intents=Intents.ALL
)

client = GatewayClient(app=bot)
