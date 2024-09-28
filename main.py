import hikari
from dotenv import dotenv_values
from time import perf_counter
import hikari.errors
from loguru import logger
from sys import stdout

logger.remove()
logger.add(sink=stdout,
           format="<level>{time:DD HH:mm:ss.SSS}</level> | <level>{level}</level> | <level>{message}</level>")

logger.level(name="INFO", color="<green>")
logger.level(name="ERROR", color="<red>")

env = dotenv_values(dotenv_path=".env", verbose=True)

bot = hikari.GatewayBot(
    token=env["BOT_TOKEN"],  # type: ignore
    intents=hikari.Intents.ALL
)


@bot.listen(hikari.StartingEvent)
async def on_ready(event: hikari.StartingEvent) -> None:
    logger.info(f"Am I alive? {bot.is_alive}")
    await bot.update_presence(activity=hikari.Activity(
        name="What's up, uB?", type=hikari.ActivityType.WATCHING))


@bot.listen(hikari.GuildMessageCreateEvent)
async def on_message(event: hikari.GuildMessageCreateEvent) -> None:
    if event.message.content == "!?ping":
        before: float = perf_counter()
        msg: hikari.Message = await event.message.respond(content="Pong!")
        ping: float = (perf_counter() - before) * 1000
        await msg.edit(content=f"Pong! 🏓 Time taken: `{int(ping)}ms`")
        logger.info(f"{event.message.author} : ping | Pong! 🏓 Time taken: {
                    int(ping)}ms")
        return

    if not event.message.author.is_bot:
        return

    guild = event.get_guild()

    try:
        if guild.get_role(int(env["BOTS_ROLE_ID"])) in event.message.member.get_roles():
            return
    except AttributeError:
        pass

    # TODO make it optional
    channel = guild.get_channel(
        channel=int(env["LOGS_CHANNEL_ID"])
    )

    try:
        await event.message.delete()
    except (hikari.errors.NotFoundError, hikari.errors.ForbiddenError):
        embed = hikari.Embed(
            title="⚠️ Error",
            description=f"Failed to delete message {
                event.message_id} from {event.message.channel_id}",
            color=0xFF0000
        )
        logger.error(f"{event.message.author} : auto | Failed to delete message {
                     event.message_id} from \x23{event.message.channel_id}")
        await bot.rest.create_message(channel=channel, embed=embed)
        return

    embed = hikari.Embed(
        title="🎉 Success",
        description=f"Deleted message {
            event.message_id} from {event.message.channel_id}",
        color=0x00FF00
    )
    logger.info(f"{event.message.author} : auto | Deleted message {
                event.message_id} from \x23{event.message.channel_id}")
    await bot.rest.create_message(channel=channel, embed=embed)


def run() -> None:
    if __name__ == "__main__":
        bot.run()


run()
