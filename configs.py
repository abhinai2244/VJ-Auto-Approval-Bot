# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01


from os import path, getenv

class Config:
    API_ID = int(getenv("API_ID", "29483517"))
    API_HASH = getenv("API_HASH", "e35a05d338376cbcd8162f810aed878d")
    BOT_TOKEN = getenv("BOT_TOKEN", "7953570607:AAE1gm-rIhTSPNncKARjnABtM2WeSi6ivHM")
    # Your Force Subscribe Channel Id Below 
    CHID = int(getenv("CHID", "-1002593166412")) # Make Bot Admin In This Channel
    # Admin Or Owner Id Below
    SUDO = list(map(int, getenv("SUDO", "5756495153").split()))
    MONGO_URI = getenv("MONGO_URI", "mongodb+srv://user1:abhinai.2244@cluster0.7oaqx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    
cfg = Config()

# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01
