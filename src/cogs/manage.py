import config 
import discord
from discord.ext import commands


class Manage(commands.Cog):
    def __init__(self, bot:discord.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("|-[COG] Manage is ready")
    
    
    manage = discord.SlashCommandGroup(
        "manage", "test group"
    )
    
    
    

def setup(bot:discord.Bot):
    return bot.add_cog(Manage(bot))