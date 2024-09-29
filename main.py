import hikari
from time import monotonic
import hikari.errors
from os import name
from asyncio import set_event_loop_policy
from uvloop import EventLoopPolicy
from vars import bot, env, logger

# flake8: noqa | something as cogs
from start_event import on_ready
from commands.ping import ping


# https://docs.hikari-py.dev/en/stable/#uvloop
if name != "nt":
    set_event_loop_policy(policy=EventLoopPolicy())


@bot.listen(hikari.GuildMessageCreateEvent)
async def on_message(event: hikari.GuildMessageCreateEvent) -> None:
    if not event.message.author.is_bot:
        return

    if event.message.webhook_id is not None:
        return

    guild = None

    guild = event.get_guild()

    try:
        if guild.get_role(int(env["BOTS_ROLE_ID"])) in event.message.member.get_roles():
            return
    except AttributeError:
        # no? that's ok
        pass

    channel: hikari.PermissibleGuildChannel | None = None

    if env["LOGS_CHANNEL_ID"] is not None:
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
        logger.error(f"{event.message.author}:auto | Failed to delete message {
                     event.message_id} from \x23{event.message.channel_id}")
        await bot.rest.create_message(channel=channel, embed=embed)
        return

    embed = hikari.Embed(
        title="🎉 Success",
        description=f"Deleted message {
            event.message_id} from {event.message.channel_id}",
        color=0x00FF00
    )
    logger.info(f"{event.message.author}:auto | Deleted message {
                event.message_id} from channel {event.message.channel_id} \n ")
    await bot.rest.create_message(channel=channel, embed=embed)


def run() -> None:
    if __name__ == "__main__":
        bot.run()


run()
