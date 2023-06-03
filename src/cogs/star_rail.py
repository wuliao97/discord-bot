import config
import pyocr
import utils.functions as funcs 
import discord
from discord.ext import commands
from PIL import Image

class StarRail(commands.Cog):
    def __init__(self, bot:discord.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("|-[COG] StarRail is ready")
    
    
    star = discord.SlashCommandGroup(
        "starrail", "", config.VERIFED_SERVERS
    )    
    
    
    @star.command(name="artifacter")
    async def starrail_arcifacter(self, inter:discord.Interaction, image:discord.Attachment):
        PATH=(config.STAR_RAIL_IMAGE + "artifacter.png")
        await image.save(PATH)    
        
        result = funcs.tesseract(PATH)
        
        
        await inter.response.send_message(result)
        



def setup(bot:discord.Bot):
    return bot.add_cog(StarRail(bot))