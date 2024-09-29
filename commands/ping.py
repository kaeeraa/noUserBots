from vars import logger, client
from arc import InteractionResponse, slash_command, GatewayContext
from time import monotonic


@client.include
@slash_command(name="ping",
               description="Check ping of bot",
               is_dm_enabled=True)
async def ping(ctx: GatewayContext) -> None:
    before: float = monotonic()
    msg: InteractionResponse = await ctx.respond(content="Pong!")
    ping: float = (monotonic() - before) * 1000
    await msg.edit(content=f"Pong! 🏓 Time taken: `{int(ping)}ms`")
    logger.info(f"{ctx.author}:ping | Pong! 🏓 Time taken: {
                int(ping)}ms")
