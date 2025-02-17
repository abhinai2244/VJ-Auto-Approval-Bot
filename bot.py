# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram import filters, Client, errors, enums
from pyrogram.errors import UserNotParticipant
from pyrogram.errors.exceptions.flood_420 import FloodWait
from database import add_user, add_group, all_users, all_groups, users, remove_user
from configs import cfg
import random, asyncio

app = Client(
    "approver",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN
)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Main process ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_chat_join_request(filters.group | filters.channel)
async def approve(_, m : Message):
    op = m.chat
    kk = m.from_user
    try:
        add_group(m.chat.id)
        await app.approve_chat_join_request(op.id, kk.id)
        await app.send_message(kk.id, "**Hello {}!\nWelcome To {}\n\n__Powerd By : @ABCMODS __**".format(m.from_user.mention, m.chat.title))
        add_user(kk.id)
    except errors.PeerIdInvalid as e:
        print("user isn't start bot(means group)")
    except Exception as err:
        print(str(err))    
 
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Start ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.private & filters.command("start"))
async def op(_, m :Message):
    try:
        await app.get_chat_member(cfg.CHID, m.from_user.id)
    except:
        try:
            invite_link = await app.create_chat_invite_link(int(cfg.CHID))
        except:
            await m.reply("**Make Sure I Am Admin In Your Channel**")
            return 
        key = InlineKeyboardMarkup(
            [[
                InlineKeyboardButton("🍿 Join Update Channel 🍿", url=invite_link.invite_link),
                InlineKeyboardButton("🍀 Check Again 🍀", callback_data="chk")
            ]]
        ) 
        await m.reply_text("**⚠️Access Denied!⚠️\n\nPlease Join My Update Channel To Use Me.If You Joined The Channel Then Click On Check Again Button To Confirm.**", reply_markup=key)
        return 
    keyboard = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("🗯 Channel", url="https://t.me/vj_botz"),
            InlineKeyboardButton("💬 Support", url="https://t.me/vj_bot_disscussion")
        ]]
    )
    add_user(m.from_user.id)
    await m.reply_photo("https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExZzJvb2N3Yjh5Z3E1cmdmNGtzOXgxa2hoN3VxbzA5a3RlZ2Fvd2Y1YyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3kuSo744UIPJjcJUEn/giphy.gif", caption="**🦊 Hello {}!\nI'm an auto approve [Admin Join Requests]({}) Bot.\nI can approve users in Groups/Channels.Add me to your chat and promote me to admin with add members permission.\n\n__Powered By : @ABCMODS__**".format(m.from_user.mention, "https://t.me/telegram/153"), reply_markup=keyboard)
    

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ callback ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_callback_query(filters.regex("chk"))
async def chk(_, cb : CallbackQuery):
    try:
        await app.get_chat_member(cfg.CHID, cb.from_user.id)
    except:
        await cb.answer("🙅‍♂️ You are not joined my channel first join channel then check again. 🙅‍♂️", show_alert=True)
        return 
    keyboard = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("🗯 Channel", url="https://t.me/ABCMODS"),
            InlineKeyboardButton("💬 Support", url="https://t.me/ABCDEVELOPER")
        ]]
    )
    add_user(m.from_user.id)
    await cb.edit_text(text="**🦊 Hello {}!\nI'm an auto approve [Admin Join Requests]({}) Bot.\nI can approve users in Groups/Channels.Add me to your chat and promote me to admin with add members permission.\n\n__Powered By : @ABCMODS __**".format(cb.from_user.mention, "https://t.me/telegram/153"), reply_markup=keyboard)
    

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ info ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("users") & filters.user(cfg.SUDO))
async def dbtool(_, m : Message):
    xx = all_users()
    x = all_groups()
    tot = int(xx + x)
    await m.reply_text(text=f"""
🍀 Chats Stats 🍀
🙋‍♂️ Users : `{xx}`
👥 Groups : `{x}`
🚧 Total users & groups : `{tot}` """)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Broadcast ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("bcast") & filters.user(cfg.SUDO))
async def bcast(_, m: Message):
    key = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("📝 Text", callback_data="bcast_text"),
            InlineKeyboardButton("📷 Photo", callback_data="bcast_photo"),
            InlineKeyboardButton("🎥 Video", callback_data="bcast_video")
        ]]
    )
    await m.reply_text("**What type of content do you want to broadcast?**", reply_markup=key)

@app.on_callback_query(filters.regex("bcast_"))
async def handle_broadcast(_, cb: CallbackQuery):
    bcast_type = cb.data.split("_")[1]
    
    if bcast_type == "text":
        await cb.message.reply_text("**Please send me the text to broadcast.**")
        await cb.answer()
        return

    if bcast_type == "photo":
        await cb.message.reply_text("**Please send me the photo with a caption to broadcast.**")
        await cb.answer()
        return

    if bcast_type == "video":
        await cb.message.reply_text("**Please send me the video with a caption to broadcast.**")
        await cb.answer()
        return

@app.on_message(filters.user(cfg.SUDO) & filters.reply)
async def send_broadcast(_, m: Message):
    allusers = users
    lel = await m.reply_text("`⚡️ Processing...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0

    # Check the type of message being broadcasted
    if m.reply_to_message.photo:
        content_type = "photo"
    elif m.reply_to_message.video:
        content_type = "video"
    elif m.reply_to_message.text:
        content_type = "text"
    else:
        await lel.edit("**Unsupported content type. Please send text, photo, or video.**")
        return

    for usrs in allusers.find():
        try:
            userid = usrs["user_id"]
            if content_type == "photo":
                await m.reply_to_message.copy(int(userid))
            elif content_type == "video":
                await m.reply_to_message.copy(int(userid))
            elif content_type == "text":
                await app.send_message(chat_id=int(userid), text=m.reply_to_message.text)
            success += 1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
        except errors.InputUserDeactivated:
            deactivated += 1
            remove_user(userid)
        except errors.UserIsBlocked:
            blocked += 1
        except Exception as e:
            failed += 1

    await lel.edit(f"✅Successfully sent to `{success}` users.\n❌ Failed to `{failed}` users.\n👾 Blocked users: `{blocked}`\n👻 Deactivated users: `{deactivated}`.")


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Broadcast Forward ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("fcast") & filters.user(cfg.SUDO))
async def fcast(_, m : Message):
    allusers = users
    lel = await m.reply_text("`⚡️ Processing...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0
    for usrs in allusers.find():
        try:
            userid = usrs["user_id"]
            #print(int(userid))
            if m.command[0] == "fcast":
                await m.reply_to_message.forward(int(userid))
            success +=1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
            if m.command[0] == "fcast":
                await m.reply_to_message.forward(int(userid))
        except errors.InputUserDeactivated:
            deactivated +=1
            remove_user(userid)
        except errors.UserIsBlocked:
            blocked +=1
        except Exception as e:
            print(e)
            failed +=1

    await lel.edit(f"✅Successfull to `{success}` users.\n❌ Faild to `{failed}` users.\n👾 Found `{blocked}` Blocked users \n👻 Found `{deactivated}` Deactivated users.")

print("I'm Alive Now!")
app.run()
