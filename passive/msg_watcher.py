from persist.vars import bot, env, logger
from hikari import (
    GatewayGuild, GuildMessageCreateEvent, Message,
    OwnUser, Snowflake, User, errors, Embed
)
from typing import Optional


async def on_message(event: GuildMessageCreateEvent) -> None:
    """
    Triggered when a message is created in a guild.

    Deletes message from not whitelisted bots.
    Also sends a message to the logs channel if the bot fails to delete the
    message.

    :param event: The event that triggered this function.
    :type event: GuildMessageCreateEvent
    """
    target: User = event.message.author
    targetMessage: Message = event.message
    botSelf: Optional[OwnUser] = bot.get_me()
    guild: Optional[GatewayGuild] = event.get_guild()
    botsRoleId: Optional[str] = env.get("BOTS_ROLE_ID")
    logsChannelId: Optional[str] = env.get("LOGS_CHANNEL_ID")

    if not botsRoleId:
        logger.error("Failed to get bots role id")
        return
    if not logsChannelId:
        logger.info("No logs channel set")
    if botSelf is None:
        logger.error("Failed to get bot instance")
        return
    if guild is None:
        logger.error("Failed to get guild instance")
        return

    botId: Snowflake = botSelf.id

    if not target.is_bot or targetMessage.webhook_id is not None:
        logger.info(f"{target}:auto | {targetMessage.content} \n Allowed")
        return

    if target.id == botId:
        return

    try:
        if guild.get_role(Snowflake(botsRoleId)):
            logger.info(f"{target}:auto | {targetMessage.content} \n Allowed")
            return
    except AttributeError:
        pass

    async def create_message(embed: Embed) -> None:
        """
        Creates a message in the given channel with the given embed.

        :param embed: The embed to be sent.
        """
        if logsChannelId:
            await bot.rest.create_message(channel=int(logsChannelId), embed=embed)

    try:
        await targetMessage.delete()
    except (errors.NotFoundError, errors.ForbiddenError):
        embed = Embed(
            title=" Error",
            description=f"Failed to delete message {
                targetMessage.id} from {targetMessage.channel_id}",
            color=0xFF0000
        )
        logger.error(f"{target}:auto | Failed to delete message {
                     targetMessage.id} from #{targetMessage.channel_id}")
        await create_message(embed=embed)
        return

    embed = Embed(
        title=" Success",
        description=f"Deleted message {
            targetMessage.id} from {targetMessage.channel_id}",
        color=0x00FF00
    )
    logger.info(f"{target}:auto | Deleted message {
                targetMessage.id} from channel {targetMessage.channel_id} \n ")
    await create_message(embed=embed)
