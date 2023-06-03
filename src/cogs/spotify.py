import config

import utils.spotifyutil as sutil
import utils.functions as funcs

import json

import discord
from discord.commands import Option
from discord.ext import commands


class SpotifyCommand(commands.Cog):
    def __init__(self, bot:discord.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("|-[COG] Spotify is ready")
    
    
    spotify = discord.SlashCommandGroup(
        "spotify", "Various Spotify command"
    )

    search = spotify.create_subgroup(
        "search", "Varuous Spotify Search command"
    )
    
    
    sjson = spotify.create_subgroup(
        "json", "Various Spotify json command"
    )
    
    
    @spotify.command(name="listening")
    async def spotify_listening(
        self,
        inter:discord.Interaction,
        user:Option(discord.Member, default=None),
        simple:Option(
            name="simple", description="No buttons?", choices=["Yes", "No"], default="No"
        )
    ):
        user:discord.Member = user or inter.user
        flag, message = sutil.spotify_check(user)
        e = discord.Embed(color=config.Spotify_green)
        
        if flag:
            spotify = sutil.Spotify(user)
            spotify_urls = sutil.Spotify_URLS(spotify)
            time = sutil.track_time(spotify.track_id)
            
            e.add_field(name="Title", value=sutil.quote(funcs.forming_string(spotify.title, spotify_urls[0]), "**"), inline=False)
            e.add_field(name="Album", value=sutil.quote(funcs.forming_string(spotify.album, spotify_urls[1]), "**"), inline=False)
            e.add_field(name="Artists", value=sutil.quote(", ".join(funcs.forming_string(spotify.artists, spotify_urls[2])), "**"), inline=False)
            e.set_author(icon_url=user.display_avatar, name="%s is Listening" % (user.display_name))
            e.set_footer(text="Time: %s | ID: %s" % (time, spotify.track_id))
            e.set_thumbnail(url=spotify.album_cover_url)
        else:
            e.description = message
        
        track_id, album_id, artists_id = sutil.extract_ids(spotify.track_id)        
        view = discord.ui.View() if funcs.YesOrNo(simple) else sutil.SpotifyDetails(track_id, album_id, artists_id)
        
        await inter.response.send_message(
            embeds=[e], view=view, ephemeral=True if flag is False else False
        )
    
    
    
    @spotify.command(name="track")
    async def spotify_track(self, inter:discord.Interaction, user:Option(discord.Member, default=None)):
        user:discord.Member = user or inter.user
        flag, message = sutil.spotify_check(user)
        
        if flag:
            spotify = sutil.Spotify(user)
            message = spotify.track_url   
            
        else:
            e = discord.Embed(
                description=message, color=config.Spotify_green
            )
            
        await inter.response.send_message(
            content=message if flag else None,
            embeds=[e] if flag is False else None, 
            ephemeral=True if flag is False else False
        )
    
    
    
    @spotify.command(name="cover")
    async def spotify_cover(self, inter:discord.Interaction, user:Option(discord.Member, default=None)):
        user:discord.Member = user or inter.user
        flag, message = sutil.spotify_check(user)
        e = discord.Embed(color=config.Spotify_green)
        
        if flag:
            spotify = sutil.Spotify(user)
            e.description = funcs.quote(funcs.forming_string(spotify.title, spotify.track_url), "**")
            e.set_author(icon_url=user.display_avatar, name="%s is Listening" % (user.display_name))
            e.set_image(url=spotify.album_cover_url)
        else:
            e.description = message
        
        await inter.response.send_message(embeds=[e], ephemeral=True if flag is False else False)
            
    
    
    
    @sjson.command(name="track")
    async def sjson_track(self, inter:discord.Interaction, trackid_or_url:Option()):
        track_id = sutil.id_or_url_check(trackid_or_url)
        spotify = sutil.spotify_api(track_id)
        fp = config.SPOTIFY + "track.json"
        
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(obj=spotify, fp=f, indent=2, ensure_ascii=False)
        
        await inter.response.send_message(file=discord.File(fp))
    
    
        
    @sjson.command(name="album")
    async def sjson_album(self, inter:discord.Interaction, albumid_or_url:Option()):
        album_id = sutil.id_or_url_check(albumid_or_url)
        spotify = sutil.spotify_api(album_id, type="album")
        fp = config.SPOTIFY + "album.json"
        
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(obj=spotify, fp=f, indent=2, ensure_ascii=False)
        
        await inter.response.send_message(file=discord.File(fp))
    
    
    
    @sjson.command(name="artist")
    async def sjson_artist(self, inter:discord.Interaction, artistid_or_url:Option()):
        artist_id = sutil.id_or_url_check(artistid_or_url)
        spotify = sutil.spotify_api(artist_id, type="artist")
        fp = config.SPOTIFY + "artist.json"
        
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(obj=spotify, fp=f, indent=2, ensure_ascii=False)
        
        await inter.response.send_message(file=discord.File(fp))
    
    
    
    @sjson.command(name="top-tracks")
    async def sjson_top_tracks(self, inter:discord.Interaction, artistid_or_url):
        artist_id = sutil.id_or_url_check(artistid_or_url)
        spotify = sutil.spotify_api(artist_id, type="top tracks")
        fp = config.SPOTIFY + "top-tracks.json"
        
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(obj=spotify, fp=f, indent=2, ensure_ascii=False)
        
        await inter.response.send_message(file=discord.File(fp))
    
    
    
    @sjson.command(name="artist-albums")
    async def sjson_top_tracks(self, inter:discord.Interaction, artistid_or_url):
        artist_id = sutil.id_or_url_check(artistid_or_url)
        spotify = sutil.spotify_api(artist_id, type="artist albums")
        fp = config.SPOTIFY + "artist-albums.json"
        
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(obj=spotify, fp=f, indent=2, ensure_ascii=False)
        
        await inter.response.send_message(file=discord.File(fp))
    


def setup(bot:discord.Bot):
    return bot.add_cog(SpotifyCommand(bot))