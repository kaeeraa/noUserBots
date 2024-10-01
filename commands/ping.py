from persist.vars import logger, client
from arc import InteractionResponse, slash_command, GatewayContext
from time import monotonic


@client.include
@slash_command(name="ping",
               description="Check ping of bot",
               is_dm_enabled=True)
async def ping(ctx: GatewayContext) -> None:
    """
    Checks the ping of the bot.

    Sends a message with the bot's ping.

    :param ctx: The context of the command.
    :type ctx: GatewayContext
    """
    before: float = monotonic()
    msg: InteractionResponse = await ctx.respond(content="Pong!")
    ping: float = (monotonic() - before) * 1000

    logger.info(f"{ctx.author}:ping | Pong! 🏓 Time taken: {
                int(ping)}ms")
    await msg.edit(content=f"Pong! 🏓 Time taken: `{int(ping)}ms`")
