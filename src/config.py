import os
import json
import dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


"""Colors"""
transparent = 0x313338
Spotify_green = 0x1DB954
Spotify_black = 0x191414



"""UTLS"""
spotify_url = "https://open.spotify.com/"




"""PATHs"""
PATH = os.path.dirname(__file__)
ROOT = PATH

RESOURCE = ROOT + os.sep + "resource" + os.sep

TX = RESOURCE + "tx" + os.sep
FONTS = RESOURCE + "fonts" + os.sep
IMAGE = RESOURCE + "image" + os.sep
STAR_RAIL_IMAGE = IMAGE + "star_rail" + os.sep

INFOR = RESOURCE + "infor" + os.sep
SPOTIFY = RESOURCE + "spotify" + os.sep
STAR_RAIL = RESOURCE + "star_rail" + os.sep



"""Dotenv"""
dotenv.load_dotenv(
    os.path.join(PATH, "config", ".env")
)

sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id     = os.environ.get("CLIENT_ID"), 
        client_secret = os.environ.get("CLIENT_SECRET")
        )
)

TOKEN = os.environ.get("TOKEN")

COGS = [
    "cogs." + cog_name[:-3] for cog_name in os.listdir(os.path.join(PATH, "cogs")) if os.path.splitext(cog_name)[1] == ".py"
]




"""JSON"""
with open(os.path.join(PATH, "config", "config.json")) as f:
    config_json = json.load(f)


VERIFED_SERVERS = config_json["verified_servers"]