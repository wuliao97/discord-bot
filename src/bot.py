import config

import discord
import asyncio
import datetime


bot = discord.Bot(
    intents=discord.Intents.all()
)


@bot.event
async def on_ready():
    print("[%s] %s on ready" % (datetime.datetime.now().strftime("%X"), bot.user))


def main():
    for cog in config.COGS:
        bot.load_extension(cog)
    
    bot.run(config.TOKEN)


if __name__ == "__main__":
    main()