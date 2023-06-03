from discord.ui.item import Item
import config
import spotipy
import discord
import dateutil

from utils.functions import quote, forming_string


class SpotifyDetails(discord.ui.View):
    def __init__(self, track_id, album_id, artists_id:list[str]):
        super().__init__()
        self.track_id = track_id
        self.album_id = album_id
        self.artists_id = artists_id    
        self.track = config.sp.track(track_id)
        self.album = config.sp.album(album_id)
        self.artists = config.sp.artists(artists_id)
    
        if 1 <= (count:=len(self.artists_id)):
            for i in range(count):
                self.add_item(SpotifyDetailsArtists(i, self.artists_id[i]))
    
    @discord.ui.button(label="Track Info", style=discord.ButtonStyle.green)
    async def track_callbacK(self, button:discord.Button, inter:discord.Interaction):
        button.disabled = True        
        await inter.response.edit_message(view=self)
        
        title = self.track["name"]
        album = self.track["album"]["name"]
        artists = extract_artsts(self.track_id, "name")
        artists_url = extract_artsts(self.track_id, "url")
        time = track_time(self.track["duration_ms"] / 1000, type="literal")
        
        e = discord.Embed(title="Track Info", color=config.Spotify_green)
        e.set_thumbnail(url=self.track["album"]["images"][0]["url"])

        e.add_field(name="Song Name", value=quote(forming_string(title, self.track["external_urls"]["spotify"]), "**"))
        e.add_field(name="Album", value=quote(forming_string(album, self.track["album"]["external_urls"]["spotify"]), "**"))
        e.add_field(name="Artists", value=quote(", ".join(forming_string(artists, artists_url)), "**"))
        
        e.add_field(name="Time", value=quote(time, "**"))
        e.add_field(name="Popularity", value=quote(self.track["popularity"], "**"))
        e.add_field(name="Release Date", value=quote(self.track["album"]["release_date"], "**"))
        
        e.add_field(name="Available Markets", value=quote(len(self.track["available_markets"]), "**"))
        e.add_field(name="ID", value=quote(self.track["id"], "**"))
        
        e.set_footer(text="isrc: %s" % (self.track["external_ids"]["isrc"]))
        
        await inter.respond(embeds=[e])
    
    
    @discord.ui.button(label="Album Info", style=discord.ButtonStyle.green)
    async def album_callback(self, button:discord.Button, inter:discord.Interaction):
        button.disabled = True
        await inter.response.edit_message(view=self)
        
        album_title = self.album["name"]
        artists = extract_artsts(self.album_id, "name", "album")
        artists_url = extract_artsts(self.album_id, "url", "album")
        time = track_time(sum([round(item["duration_ms"] / 1000) for item in self.album["tracks"]["items"]]), "literal")
        
        e = discord.Embed(title="Album Info", color=config.Spotify_green)
        e.set_thumbnail(url=self.album["images"][0]["url"])
        
        e.add_field(name="Album Name", value=quote(forming_string(album_title, self.album["external_urls"]["spotify"]), "**"))
        e.add_field(name="Artists", value=quote(", ".join(forming_string(artists, artists_url)), "**"))
        e.add_field(name="Total Tracks", value=quote(self.album["total_tracks"], "**"))
        
        e.add_field(name="Time", value=quote(time, "**"))
        e.add_field(name="Popularity", value=quote(self.album["popularity"], "**"))
        e.add_field(name="Release Date", value=quote(self.album["release_date"], "**"))
        
        e.add_field(name="Genres", value=quote(", ".join(self.album["genres"]), "**"), inline=False)
        
        e.add_field(name="Available Markets", value=quote(len(self.album["available_markets"]), "**"))
        e.add_field(name="ID", value=quote(self.album["id"], "**"))
        e.add_field(name="Copyright", value=quote(self.album["copyrights"][0]["text"], "**"))
        
        e.set_footer(text="External Ids: %s" % (self.album["external_ids"]["upc"]))
        
        await inter.respond(embeds=[e])



class SpotifyDetailsArtists(discord.ui.Button):
    def __init__(self, count, artist_id):
        super().__init__(label="Artist Info %s" % (count + 1) if count != 0 else "Artist Info ", style=discord.ButtonStyle.green)
        self.count = count
        self.artist_id = artist_id
        
    async def callback(self, inter:discord.Interaction):
        self.disabled = True
        await inter.response.edit_message(view=self)
        
        artist = spotify_api(self.artist_id, type="artist")
        
        artist_albums = spotify_api(self.artist_id, "artist albums")
        artist_albums = [track for track in artist_albums["items"] if track["artists"][0]["id"] == self.artist_id]
        
        e = discord.Embed(title="Artist Info", color=config.Spotify_green)
        e.set_thumbnail(url=artist["images"][0]["url"])
        
        e.add_field(name="Artist Name", value=quote(forming_string(artist["name"], artist["external_urls"]["spotify"]), "**"))
        e.add_field(name="Followes", value=quote(artist["followers"]["total"], "**"))
        e.add_field(name="Total Albums", value=quote(len(artist_albums), "**"))
        
        e.add_field(name="Popularity", value=quote(artist["popularity"], "**"))
        
        e.add_field(name="Genres", value=quote(", ".join(artist["genres"]), "**"), inline=False)
        
        top_tracks = spotify_api(self.artist_id, "top tracks")
        top_tracks_name, top_tracks_url = (track["name"] for track in top_tracks["tracks"]), (track["external_urls"]["spotify"] for track in top_tracks["tracks"])
        e.add_field(name="Top Tracks", value=quote(",".join(forming_string(top_tracks_name, top_tracks_url)), "**"))
        
        await inter.response.send_message(embeds=[e])



def extract_artsts(id:str, key:str="name", type="track"):
    obj = spotify_api(id, type=type)
    
    if key=="url":
        return [artist["external_urls"]["spotify"] for artist in obj["artists"]]
    
    return [artist[key] for artist in obj["artists"]]




def spotify_api(id:str, type:str="track", key=None):
    match (type):
        case "track":
            obj = config.sp.track(id)
        
        case "album":
            obj = config.sp.album(id)
        
        case "artist":
            obj = config.sp.artist(id)
        
        case "top tracks":
            obj = config.sp.artist_top_tracks(id, "JP")
        
        case "artist albums":
            obj = config.sp.artist_albums(id, limit=50)
        
        case _:
            raise ValueError
        
    if key:
        obj = obj[key]
    
    return obj



def extract_ids(track_id):
    spotify = spotify_api(track_id)
    
    return track_id, spotify["album"]["id"], [artist["id"] for artist in spotify["artists"]]




def user_activities_check(user:discord.Member):
    return next((activity for activity in user.activities if isinstance(activity, discord.Spotify)), None)


def spotify_check(user:discord.Member):
    flag = False
    message = user.mention

    if user.status in ("offline", "invisible"):
        message += " is offline right now!" 
    
    elif not user_activities_check(user):
        message += " is not listening a Spotify!"
    
    else:
        flag = True
    
    return flag, message


def Spotify(user:discord.Member):
    return user_activities_check(user)



def Spotify_URLS(Spotify:discord.Spotify):
    result = config.sp.track(Spotify.track_id)
    material = [result['external_urls']['spotify']]
    material.append(result['album']['external_urls']['spotify'])
    material.append([artist['external_urls']['spotify'] for artist in result['artists']])
    return material



def track_time__(material:discord.Spotify):
    """Old function"""
    return dateutil.parser.parse(str(material.duration)).strftime('%M:%S')



def track_time(obj:str, type:str="api"):
    def forming(time_obj):
        return time_obj if len(str(time_obj)) > 1 else "0" + str(time_obj)
    
    if type == "api":
        spotify = spotify_api(obj)
        duration_ms = spotify["duration_ms"] / 1000
        
    elif type == "literal":
        duration_ms = obj
    
    
    m, s = divmod(duration_ms, 60)
    h, m = divmod(m, 60)
    
    
    if duration_ms > 3600:
        return "%s:%s:%s" % (forming(round(h)), forming(round(m)), forming(round(s)))
    else:
        return "%s:%s" % (forming(round(m)), forming(int(s)))




def id_or_url_check(id_or_url:str):
    if id_or_url.startswith(config.spotify_url):
        id_or_url = id_or_url.replace(config.spotify_url, "")

    return id_or_url