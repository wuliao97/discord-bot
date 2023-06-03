import os
import pyocr
import discord
from typing import Any

from PIL import Image


def tesseract(Image_path:str, number:int=6):
    if os.name == "nt":
        pyocr.tesseract.TESSERACT_CMD = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    else:
        pyocr.tesseract.TESSERACT_CMD = r"/usr/bin/tesseract"
        # sudo apt -y install tesseract-ocr tesseract-ocr-jpn libtesseract-dev libleptonica-dev tesseract-ocr-script-jpan tesseract-ocr-script-jpan-vert 
    
    tools = pyocr.get_available_tools()
    
    builder = pyocr.builders.TextBuilder(tesseract_layout=number)
    return tools[0].image_to_string(Image.open(Image_path).convert("L"), lang="jpn", builder=builder)




def extract(obj:Any | discord.Member | discord.Guild, key:str):
    urls = {}
    
    match (key):
        case "avatar":
            urls["Avatar"] = obj.display_avatar
            
            if obj.avatar != obj.display_avatar:
                urls["Server Avatar"] = obj.avatar
            
        case "banner":
            urls["Banner"] = obj.banner
        
        case "User":
            urls["Avatar"] = obj.display_avatar
            
            if obj.avatar != obj.display_avatar:
                urls["Server Avatar"] = obj.avatar
            
            urls["Banner"] = obj.banner.url
        
        case "server" | "guild":
            urls["Icon"] = obj.icon
            
            if obj.banner:
                urls["Banner"] = obj.banner
            
            if obj.splash:
                urls["Splash"] = obj.splash.url
    
    return urls



def forming_string(val1:list, val2:list=None):
    if isinstance(val1, dict):
        val1, val2 = [i for i in val1.keys()], [i for i in val1.values()]
    
    elif isinstance(val1, str) and isinstance(val2, str):
        return "[%s](%s)" % (val1, val2) 
    
    return ["[%s](%s)" % (item1, item2) for item1, item2 in zip(val1, val2)]



def quote(literal:str, symbol:str=""):
    return ">>> %s%s%s" % (symbol, literal, symbol)



def codeblock(literal:str, lang=""):
    return "```%s\n%s```" % (lang, literal)



def YesOrNo(args:str):
    return True if args.lower() == "yes" else False