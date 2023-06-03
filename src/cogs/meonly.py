import config

import discord
from discord.ext import commands


class MeOnly(commands.Cog):
    def __init__(self, bot:discord.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("|-[COG] MeOnly is ready")
    
        
    admin = discord.SlashCommandGroup(
        "meonly", "", config.VERIFED_SERVERS
    )    
    
    
    
    

def setup(bot:discord.Bot):
    return bot.add_cog(MeOnly(bot))