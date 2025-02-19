from pymongo import MongoClient
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram import filters, Client, errors, enums
from pyrogram.errors import UserNotParticipant
from pyrogram.errors.exceptions.flood_420 import FloodWait
from database import add_user, add_group, all_users, all_groups, users, remove_user
from configs import cfg
import random, asyncio

# Initialize Pyrogram Client
app = Client(
    "approver",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN
)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Main Process ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_chat_join_request(filters.group | filters.channel)
async def approve(_, m: Message):
    try:
        add_group(m.chat.id)
        await app.approve_chat_join_request(m.chat.id, m.from_user.id)
        await app.send_message(
            m.from_user.id,
            f"**Hello {m.from_user.mention}!\nWelcome To {m.chat.title}\n\n__Powered by: @ABCMODS__**"
        )
        add_user(m.from_user.id)
    except errors.PeerIdInvalid:
        print("User has not started the bot (means group)")
    except Exception as err:
        print(str(err))

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Start Command ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.private & filters.command("start"))
async def op(_, m: Message):
    try:
        await app.get_chat_member(cfg.CHID, m.from_user.id)
    except UserNotParticipant:
        try:
            invite_link = await app.create_chat_invite_link(int(cfg.CHID))
        except:
            await m.reply("**Make sure I am an admin in your channel.**")
            return 

        key = InlineKeyboardMarkup(
            [[
                InlineKeyboardButton("🍿 Join Update Channel 🍿", url=invite_link.invite_link),
                InlineKeyboardButton("🍀 Check Again 🍀", callback_data="chk")
            ]]
        )
        await m.reply_text(
            "**⚠️ Access Denied! ⚠️\n\nPlease join my update channel to use me. If you joined the channel, click on Check Again.**",
            reply_markup=key
        )
        return

    keyboard = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("🗯 Channel", url="https://t.me/ABCMODS"),
            InlineKeyboardButton("💬 Support", url="https://t.me/ABCDEVLOPER")
        ]]
    )
    add_user(m.from_user.id)
    await m.reply_photo(
        "https://ibb.co/TqFrVzZZ",
        caption=f"**🦊 Hello {m.from_user.mention}!\nI'm an auto-approve [Admin Join Requests](https://t.me/telegram/153) Bot.\nI can approve users in Groups/Channels. Add me to your chat and promote me to admin with add members permission.\n\n__Powered by: @ABCMODS__**",
        reply_markup=keyboard
    )

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Callback Query ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_callback_query(filters.regex("chk"))
async def chk(_, cb: CallbackQuery):
    try:
        await app.get_chat_member(cfg.CHID, cb.from_user.id)
    except:
        await cb.answer(
            "🙅‍♂️ You are not joined my channel. First join the channel, then check again. 🙅‍♂️",
            show_alert=True
        )
        return

    keyboard = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("🗯 Channel", url="https://t.me/ABCMODS"),
            InlineKeyboardButton("💬 Support", url="https://t.me/ABCDEVLOPER")
        ]]
    )
    add_user(cb.from_user.id)
    await cb.edit_message_text(
        text=f"**🦊 Hello {cb.from_user.mention}!\nI'm an auto-approve [Admin Join Requests](https://t.me/telegram/153) Bot.\nI can approve users in Groups/Channels. Add me to your chat and promote me to admin with add members permission.\n\n__Powered by: @ABCMODS__**",
        reply_markup=keyboard
    )

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Info Command ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("users") & filters.user(cfg.SUDO))
async def dbtool(_, m: Message):
    total_users = all_users()
    total_groups = all_groups()
    total = total_users + total_groups
    await m.reply_text(
        text=f"""
🍀 **Chat Stats** 🍀
🙋‍♂️ Users: `{total_users}`
👥 Groups: `{total_groups}`
🚧 Total users & groups: `{total}`
"""
    )

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Broadcast ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("bcast") & filters.user(cfg.SUDO))
async def bcast(_, m : Message):
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
            if m.command[0] == "bcast":
                await m.reply_to_message.copy(int(userid))
            success +=1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
            if m.command[0] == "bcast":
                await m.reply_to_message.copy(int(userid))
        except errors.InputUserDeactivated:
            deactivated +=1
            remove_user(userid)
        except errors.UserIsBlocked:
            blocked +=1
        except Exception as e:
            print(e)
            failed +=1

    await lel.edit(f"✅Successfull to `{success}` users.\n❌ Faild to `{failed}` users.\n👾 Found `{blocked}` Blocked users \n👻 Found `{deactivated}` Deactivated users.")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Forward Broadcast ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("fcast") & filters.user(cfg.SUDO))
async def fcast(_, m: Message):
    lel = await m.reply_text("`⚡️ Processing...`")

    success, failed, deactivated, blocked = 0, 0, 0, 0
    allusers = users.find()

    for user in allusers:
        try:
            user_id = user["user_id"]
            if m.command[0] == "fcast":
                await m.reply_to_message.forward(int(user_id))
            success += 1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
        except errors.InputUserDeactivated:
            deactivated += 1
            remove_user(user_id)
        except errors.UserIsBlocked:
            blocked += 1
        except Exception:
            failed += 1

    await lel.edit(
        f"✅ Successfully forwarded to `{success}` users.\n"
        f"❌ Failed to forward to `{failed}` users.\n"
        f"👾 Blocked users: `{blocked}`\n"
        f"👻 Deactivated users: `{deactivated}`."
    )

print("I'm Alive Now!")
app.run()
