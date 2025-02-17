# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01


from os import path, getenv

class Config:
    API_ID = int(getenv("API_ID", "27152769"))
    API_HASH = getenv("API_HASH", "b98dff566803b43b3c3120eec537fc1d")
    BOT_TOKEN = getenv("BOT_TOKEN", "7117598011:AAFUFRih1s3KxCqLXWUEx1PF4f4jSLXUVCk")
    # Your Force Subscribe Channel Id Below 
    CHID = int(getenv("CHID", "-1002446190606")) # Make Bot Admin In This Channel
    # Admin Or Owner Id Below
    SUDO = list(map(int, getenv("SUDO", "5756495153,5828813546").split()))
    MONGO_URI = getenv("MONGO_URI", "mongodb+srv://user1:abhinai.2244@cluster0.7oaqx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    
cfg = Config()

# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01
