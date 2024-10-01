import hikari
from time import monotonic
import hikari.errors
from os import name
from asyncio import set_event_loop_policy
from uvloop import EventLoopPolicy
from persist.vars import bot, env, logger

# flake8: noqa | something as cogs
from passive.start_event import on_ready
from passive.msg_watcher import on_message
from commands.ping import ping

# subscribe to imported event funcs
bot.event_manager.subscribe(hikari.StartedEvent, on_ready)
bot.event_manager.subscribe(hikari.GuildMessageCreateEvent, on_message)


# https://docs.hikari-py.dev/en/stable/#uvloop
if name != "nt":
    try:
        import uvloop
    except ImportError:
        pass
    else:
        logger.info("Using uvloop")
        set_event_loop_policy(policy=EventLoopPolicy())


def run() -> None:
    """
    Runs the bot.

    This function is only called when this script is run directly, rather than
    being imported.
    """
    if __name__ == "__main__":
        bot.run()


run()
