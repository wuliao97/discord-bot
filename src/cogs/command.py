import config

from utils.functions import extract, forming_string, tesseract, codeblock

import discord
from discord.commands import Option
from discord.ext import commands

from discord_timestamps import format_timestamp 
from discord_timestamps.formats import TimestampType as tt

class Command(commands.Cog):
    def __init__(self, bot:discord.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("|-[COG] Command is ready")
    
    
    user_cmd = discord.SlashCommandGroup(
        "user", "various user command"
    )
    
    server_cmd = discord.SlashCommandGroup(
        "server", "various server command"
    )
    
    image = discord.SlashCommandGroup(
        "image", "Various Image command"
    )
    
    
    
    @user_cmd.command(name="avatar")
    async def user_avatar(self, inter:discord.Interaction, user:Option(discord.Member, default=None)):
        user:discord.Member = user or inter.user
        
        e = discord.Embed(
            description="**%s's Avatar**" % (user.mention), color=config.transparent
        )
        e.set_image(url=user.display_avatar)
        
        if user.display_avatar != user.avatar:
            e.set_thumbnail(url=user.avatar)
        
        context = forming_string(extract(user, "avatar"))
        e.add_field(name="URLs", value="> %s" % (", ".join(context)))
    
        await inter.response.send_message(embeds=[e])
    
    
    @user_cmd.command(name="banner")
    async def user_banner(self, inter:discord.Interaction, user:Option(discord.Member, default=None)):
        user:discord.Member =  await self.bot.fetch_user(user.id if user else inter.user.id)
        
        e = discord.Embed(
            color=config.transparent
        )
        
        if user.banner:
            flag = False
            context = forming_string(extract(user, "banner"))
            e.description="**%s's Banner**" % (user.mention)
            e.add_field(name="URLs", value="> %s" % ("".join(context)))
            e.set_image(url=user.banner.url)
        
        else:
            flag = True
            e.description="%s haven't the banner"

        await inter.response.send_message(embeds=[e], ephemeral=flag)
    
    
    @user_cmd.command(name="information")
    async def user_information(self, inter:discord.Interaction, user:Option(discord.Member, default=None)):
        user:discord.Member = user or inter.user
        user_ = await self.bot.fetch_user(user.id)
        
        status = str(user.status)
        status_icon = "🟢" if status == "online" else "🟡" if status == "idle" else "🔴" if status == "dnd" else "⚫"
        
        e = discord.Embed(
            description="**%s's information**" % (user.mention), color=config.transparent
        )
        e.add_field(name="Name", value="> **%s**" % (user.name))
        e.add_field(name="Discriminator", value="> **%s**" % (user.discriminator))
        e.add_field(name="ID", value="> **%s**" % (user.id))
        
        if user.display_name != user.name:
            e.add_field(name="Nickname", value="> **%s**" % (user.display_name))
            
        e.add_field(name="Bot?", value="> **%s**" % ("Yes" if user.bot else "No"))
        
        
        e.add_field(name="Status (%s)" % (status_icon), value="> **%s**" % (status))
        
        if (role_count:=len(user.roles)) > 0:
            role_list = [role.mention for role in user.roles[1:]][::-1]
            e.add_field(name="Roles (%s)" % (role_count), value="> %s" % (" ".join(role_list)), inline=False)
        
        e.add_field(name="Created Date", value="> **%s**" % (format_timestamp(user.created_at.timestamp(), tt.RELATIVE)))
        
        if inter.guild:
            e.add_field(name="Joined Date", value="> **%s**" % (format_timestamp(user.joined_at.timestamp(), tt.RELATIVE)))
        
        e.set_thumbnail(url=user.display_avatar)
        
        if user_.banner:
            e.set_image(url=user_.banner.url)
        
        
        await inter.response.send_message(embeds=[e])
    
    
    
    @server_cmd.command(name="information")
    async def server_information(self,  inter:discord.Interaction):
        guild = inter.guild
        refer  = await self.bot.http.request(discord.http.Route("GET", "/guilds/" + str(guild.id)))
        tchannels, vchannels = len(guild.text_channels), len(guild.voice_channels)
        emojis   , emojis_g  = len(guild.emojis)       , sum([1 for e in guild.emojis if e.animated])
        inside  = format_timestamp(guild.created_at.timestamp(), tt.RELATIVE)
        outside = format_timestamp(guild.created_at.timestamp(), tt.SHORT_DATE)
        
        embed = discord.Embed(title=guild.name, color=config.transparent)
        embed.add_field(name="👑 Owner",    value=guild.owner.mention)
        embed.add_field(name="🆔 ID",       value=guild.id)
        embed.add_field(name="🗓️ Creation", value=f"{outside}({inside})")
        
        embed.add_field(
            name=f"👥 Members ({guild.member_count})", 
            value="**%s** User | **%s** Bot\n**%s** Online(user)" % (
                user_:=sum(1 for user in guild.members if not user.bot),
                guild.member_count-user_,
                sum(1 for member in guild.members if member.status != discord.Status.offline and not member.bot)
            )
        )
        
        embed.add_field(
            name= f"🗨️ Channels ({tchannels + vchannels})", 
            value= "**%s** Text | **%s** Voice\n**%s** Category" % (tchannels, vchannels, len(guild.categories)))
        
        embed.add_field(
            name = f"😀 Emojis ({emojis})",
            value= "**%s** Static\n**%s** Animated\n**%s** Sticker" % (emojis-emojis_g, emojis_g, len(guild.stickers)))
        
        embed.add_field(name = "🛡️ Role", value= "**%s** Count" % (len(guild.roles)))
        
        if (guild.premium_subscription_count > 0):
            embed.add_field(name  = f"💎Boost ({guild.premium_subscription_count})", value = "**%s** Tier" % (guild.premium_tier))
        
        if (guild.icon):
            embed.set_thumbnail(url=guild.icon.url)
        
        if vanity:=refer["vanity_url_code"]:
            embed.add_field(name="🔗 Vanity", value=f"`{vanity}`")
        
        urls = extract(guild, "server")
        embed.add_field(
            name  = "URLs",
            value = ">>> " + ", ".join([f"[{k}]({v})" for k,v in urls.items()]),
            inline = False
        )
        
        if guild.banner:
            embed.set_image(url=guild.banner.url)
            
        await inter.response.send_message(embed=embed)
    
    
    @server_cmd.command(name="images")
    async def server_images(self, inter:discord.Interaction):
        urls = extract(inter.guild, "guild")
        es = [
            discord.Embed(
                description=">>> " + ", ".join(forming_string(urls)), color=config.transparent
            ).set_image(url=urls["Banner"]).set_thumbnail(url=urls["Icon"])
        ]
        es.append(
            discord.Embed(color=config.transparent).set_image(url=urls["Splash"])
        )
        
        await inter.response.send_message(embeds=es)
    
    
    
    @image.command(name="tesseract")
    async def image_tesseract(self, inter:discord.Interaction, image:Option(discord.Attachment), number:int=6):
        PATH = config.IMAGE + "image.png"
        await image.save(PATH)
        
        result = tesseract(PATH, number)
        
        e = discord.Embed(description=codeblock(result))
        e.set_thumbnail(url="attachment://" + "material.png")
        
        await inter.response.send_message(embeds=[e], file=discord.File(PATH, filename="material.png"))


def setup(bot:discord.Bot):
    return bot.add_cog(Command(bot))