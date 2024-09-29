from vars import bot, env, logger
from hikari import GuildMessageCreateEvent, PermissibleGuildChannel, errors, Embed


async def on_message(event: GuildMessageCreateEvent) -> None:
    if not event.message.author.is_bot:
        logger.info(f"{event.message.author}:auto | {
                    event.message.content} \n Allowed")
        return

    if event.message.author.id == bot.get_me().id:
        return

    if event.message.webhook_id is not None:
        logger.info(f"{event.message.author}:auto | {
                    event.message.content} \n Allowed")
        return

    guild = None

    guild = event.get_guild()

    try:
        if guild.get_role(int(env["BOTS_ROLE_ID"])) in event.message.member.get_roles():
            logger.info(f"{event.message.author}:auto | {
                        event.message.content} \n Allowed")
            return
    except AttributeError:
        # no? that's ok
        pass

    channel: PermissibleGuildChannel | None = None

    if env["LOGS_CHANNEL_ID"] is not None:
        channel = guild.get_channel(
            channel=int(env["LOGS_CHANNEL_ID"])
        )

    try:
        await event.message.delete()
    except (errors.NotFoundError, errors.ForbiddenError):
        embed = Embed(
            title="⚠️ Error",
            description=f"Failed to delete message {
                event.message_id} from {event.message.channel_id}",
            color=0xFF0000
        )
        logger.error(f"{event.message.author}:auto | Failed to delete message {
                     event.message_id} from \x23{event.message.channel_id}")
        await bot.rest.create_message(channel=channel, embed=embed)
        return

    embed = Embed(
        title="🎉 Success",
        description=f"Deleted message {
            event.message_id} from {event.message.channel_id}",
        color=0x00FF00
    )
    logger.info(f"{event.message.author}:auto | Deleted message {
                event.message_id} from channel {event.message.channel_id} \n ")
    await bot.rest.create_message(channel=channel, embed=embed)
