from pymongo import MongoClient
from pyrogram import Client, filters, errors
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import FloodWait
from database import add_user, add_group, remove_user, all_users
from configs import cfg
import asyncio

# Initialize MongoDB client and users collection
client = MongoClient(cfg.MONGO_URI)
users = client['main']['users']
groups = client['main']['groups']

app = Client("approver", api_id=cfg.API_ID, api_hash=cfg.API_HASH, bot_token=cfg.BOT_TOKEN)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Main Process ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_chat_join_request(filters.group | filters.channel)
async def approve(_, m: Message):
    op = m.chat
    kk = m.from_user
    try:
        add_group(m.chat.id)
        await app.approve_chat_join_request(op.id, kk.id)
        await app.send_message(kk.id, f"**Hello {m.from_user.mention}!\nWelcome to {m.chat.title}\n\n__Powered by: @ABCMODS__**")
        add_user(kk.id)
    except errors.PeerIdInvalid:
        print("User isn't started the bot (meaning the group).")
    except Exception as err:
        print(str(err))

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Start Command ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.private & filters.command("start"))
async def op(_, m: Message):
    try:
        await app.get_chat_member(cfg.CHID, m.from_user.id)
    except:
        try:
            invite_link = await app.create_chat_invite_link(int(cfg.CHID))
        except:
            await m.reply("**Make sure I am an Admin in your Channel.**")
            return
        key = InlineKeyboardMarkup(
            [[
                InlineKeyboardButton("🍿 Join Update Channel 🍿", url=invite_link.invite_link),
                InlineKeyboardButton("🍀 Check Again 🍀", callback_data="chk")
            ]]
        )
        await m.reply_text("**⚠️ Access Denied! ⚠️\n\nPlease Join My Update Channel To Use Me. If You Joined, Click on Check Again Button to Confirm.**", reply_markup=key)
        return
    keyboard = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("🗯 Channel", url="https://t.me/ABCMODS"),
            InlineKeyboardButton("💬 Support", url="https://t.me/ABCDEVLOPER")
        ]]
    )
    add_user(m.from_user.id)
 await m.reply_photo("https://ibb.co/TqFrVzZZ", caption=f"**🦊 Hello {m.from_user.mention}!\nI'm an auto-approve [Admin Join Requests](https://t.me/telegram/153) Bot.\nI can approve users in Groups/Channels. Add me to your chat and promote me to admin with add members permission.\n\n__Powered by: @ABCMODS__**", reply_markup=keyboard)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Callback ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_callback_query(filters.regex("chk"))
async def chk(_, cb: CallbackQuery):
    try:
        await app.get_chat_member(cfg.CHID, cb.from_user.id)
    except:
        await cb.answer("🙅‍♂️ You are not joined my channel. Please join the channel and check again.", show_alert=True)
        return
    keyboard = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("🗯 Channel", url="https://t.me/ABCMODS"),
            InlineKeyboardButton("💬 Support", url="https://t.me/ABCDEVELOPER")
        ]]
    )
    add_user(cb.from_user.id)
    await cb.edit_text(f"**🦊 Hello {cb.from_user.mention}!\nI'm an auto-approve [Admin Join Requests]({}) Bot.\nI can approve users in Groups/Channels. Add me to your chat and promote me to admin with add members permission.\n\n__Powered by: @ABCMODS__**".format("https://t.me/telegram/153"), reply_markup=keyboard)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Info ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("users") & filters.user(cfg.SUDO))
async def dbtool(_, m: Message):
    xx = all_users()
    x = all_groups()
    tot = int(xx + x)
    await m.reply_text(f"🍀 Chats Stats 🍀\n🙋‍♂️ Users: `{xx}`\n👥 Groups: `{x}`\n🚧 Total users & groups: `{tot}`")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Broadcast ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("bcast") & filters.user(cfg.SUDO))
async def bcast(_, m: Message):
    key = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("📝 Text", callback_data="bcast_text")
        ]]
    )
    await m.reply_text("**What type of content do you want to broadcast?**", reply_markup=key)


@app.on_callback_query(filters.regex("bcast_"))
async def handle_broadcast(_, cb: CallbackQuery):
    bcast_type = cb.data.split("_")[1]  # Extract the type (text)
    
    if bcast_type == "text":
        await cb.message.edit_text("**Please send me the text you want to broadcast to all users.**")
        await cb.answer()  # Acknowledge the button press

        @app.on_message(filters.user(cb.from_user.id) & filters.text)
        async def handle_text_reply(_, msg: Message):
            broadcast_text = msg.text  # Get the text the admin sent
            lel = await msg.reply_text("`⚡️ Processing...`")  # "Processing..." message

            success = 0
            failed = 0
            deactivated = 0
            blocked = 0

            allusers = all_users()

            total_users = len(allusers)
            if total_users == 0:
                await lel.edit("**No users found in the database.**")
                return

            for usrs in allusers:
                try:
                    user_id = usrs["user_id"]
                    await app.send_message(chat_id=int(user_id), text=broadcast_text)
                    success += 1
                except FloodWait as ex:
                    await asyncio.sleep(ex.value)
                except errors.InputUserDeactivated:
                    deactivated += 1
                    remove_user(user_id)
                except errors.UserIsBlocked:
                    blocked += 1
                except Exception as e:
                    failed += 1

            await lel.edit(f"✅ Successfully sent to `{success}` users.\n❌ Failed to send to `{failed}` users.\n👾 Blocked users: `{blocked}`\n👻 Deactivated users: `{deactivated}`.")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Broadcast Forward ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("fcast") & filters.user(cfg.SUDO))
async def fcast(_, m: Message):
    allusers = users
    lel = await m.reply_text("`⚡️ Processing...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0
    for usrs in allusers.find():
        try:
            userid = usrs["user_id"]
            if m.command[0] == "fcast":
                await m.reply_to_message.forward(int(userid))
            success += 1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
            if m.command[0] == "fcast":
                await m.reply_to_message.forward(int(userid))
        except errors.InputUserDeactivated:
            deactivated += 1
            remove_user(userid)
        except errors.UserIsBlocked:
            blocked += 1
        except Exception as e:
            failed += 1

    await lel.edit(f"✅ Successfully sent to `{success}` users.\n❌ Failed to send to `{failed}` users.\n👾 Found `{blocked}` Blocked users.\n👻 Found `{deactivated}` Deactivated users.")

print("Bot is running!")
app.run()
