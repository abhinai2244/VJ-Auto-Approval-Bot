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
async def approve(_, m: Message):
    op = m.chat
    kk = m.from_user
    try:
        add_group(m.chat.id)
        await app.approve_chat_join_request(op.id, kk.id)
        await app.send_message(kk.id, f"**Hello {m.from_user.mention}!\nWelcome To {m.chat.title}\n\n__Powered By : @ABCMODS__**")
        add_user(kk.id)
    except errors.PeerIdInvalid:
        print("User hasn't started the bot or invalid peer.")
    except Exception as err:
        print(str(err))

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Start ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.private & filters.command("start"))
async def op(_, m: Message):
    try:
        await app.get_chat_member(cfg.CHID, m.from_user.id)
    except:
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
        await m.reply_text("**⚠️Access Denied!⚠️\n\nPlease join my update channel to use me. If you joined the channel, click the 'Check Again' button to confirm.**", reply_markup=key)
        return

    keyboard = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("🗯 Channel", url="https://t.me/ABCMODS"),
            InlineKeyboardButton("💬 Support", url="https://t.me/clutch008")
        ]]
    )
    add_user(m.from_user.id)
    await m.reply_photo("https://ibb.co/b5vpmdyj", caption=f"**🦊 Hello {m.from_user.mention}!\nI'm an auto-approve [Admin Join Requests](https://t.me/telegram/153) bot.\nAdd me to your chat and promote me to admin with 'Add Members' permission.\n\n__Powered By : @ABCMODS__**", reply_markup=keyboard)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Callback ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_callback_query(filters.regex("chk"))
async def chk(_, cb: CallbackQuery):
    try:
        await app.get_chat_member(cfg.CHID, cb.from_user.id)
    except:
        await cb.answer("🙅‍♂️ You are not joined my channel. First join the channel and then check again. 🙅‍♂️", show_alert=True)
        return
    keyboard = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("🗯 Channel", url="https://t.me/ABCMODS"),
            InlineKeyboardButton("💬 Support", url="https://t.me/clutch008")
        ]]
    )
    await cb.edit_message_text(text=f"**🦊 Hello {cb.from_user.mention}!\nI'm an auto-approve [Admin Join Requests](https://t.me/telegram/153) bot.\nAdd me to your chat and promote me to admin with 'Add Members' permission.\n\n__Powered By : @ABCMODS__**", reply_markup=keyboard)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Users Stats ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("users") & filters.user(cfg.SUDO))
async def dbtool(_, m: Message):
    xx = all_users()
    x = all_groups()
    tot = int(xx + x)
    await m.reply_text(text=f"""
🍀 Chats Stats 🍀
🙋‍♂️ Users: `{xx}`
👥 Groups: `{x}`
🚧 Total users & groups: `{tot}` """)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Broadcast ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("bcast") & filters.user(cfg.SUDO))
async def bcast(_, m: Message):
    if not m.reply_to_message:
        await m.reply("Please reply to a message to broadcast.")
        return
    allusers = users.find()
    lel = await m.reply_text("`⚡️ Processing...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0

    for usrs in allusers:
        userid = usrs["user_id"]
        try:
            await m.reply_to_message.copy(int(userid))
            success += 1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
            await m.reply_to_message.copy(int(userid))
        except errors.InputUserDeactivated:
            deactivated += 1
            remove_user(userid)
        except errors.UserIsBlocked:
            blocked += 1
        except Exception as e:
            print(f"Error with user {userid}: {e}")
            failed += 1

    await lel.edit(f"✅ Successfully sent to `{success}` users.\n❌ Failed to `{failed}` users.\n👾 Blocked by `{blocked}` users.\n👻 Found `{deactivated}` deactivated users.")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Broadcast Forward ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("fcast") & filters.user(cfg.SUDO))
async def fcast(_, m: Message):
    if not m.reply_to_message:
        await m.reply("Please reply to a message to forward.")
        return
    allusers = users.find()
    lel = await m.reply_text("`⚡️ Processing...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0

    for usrs in allusers:
        userid = usrs["user_id"]
        try:
            await m.reply_to_message.forward(int(userid))
            success += 1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
            await m.reply_to_message.forward(int(userid))
        except errors.InputUserDeactivated:
            deactivated += 1
            remove_user(userid)
        except errors.UserIsBlocked:
            blocked += 1
        except Exception as e:
            print(f"Error with user {userid}: {e}")
            failed += 1

    await lel.edit(f"✅ Successfully forwarded to `{success}` users.\n❌ Failed to `{failed}` users.\n👾 Blocked by `{blocked}` users.\n👻 Found `{deactivated}` deactivated users.")

print("I'm Alive Now!")
app.run()
