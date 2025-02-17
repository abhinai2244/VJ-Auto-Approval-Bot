import logging
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram import filters, Client, errors, enums
from pyrogram.errors import UserNotParticipant
from pyrogram.errors.exceptions.flood_420 import FloodWait
from database import add_user, add_group, all_users, all_groups, users, remove_user
from configs import cfg
import random, asyncio
import os

# Setup logging to a file
logging.basicConfig(filename="broadcast_log.txt", level=logging.INFO, format='%(asctime)s - %(message)s')

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

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Broadcast ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("bcast") & filters.user(cfg.SUDO))
async def bcast(_, m: Message):
    # Prompt for the broadcast message
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("CANCEL", callback_data="cancel_broadcast")],
            [InlineKeyboardButton("CLOSE", callback_data="close_broadcast")]
        ]
    )
    prompt_message = await m.reply("Give me a broadcast message:", reply_markup=keyboard)

    # Wait for the admin's response
    try:
        response = await app.listen(m.chat.id, timeout=300)
    except asyncio.TimeoutError:
        await prompt_message.edit("Timeout: No response received. Broadcast cancelled.")
        return

    # Check if the admin canceled the process
    if response.text and response.text.lower() == "cancel":
        await prompt_message.edit("Broadcast cancelled.")
        return

    # Get the message or media to broadcast
    broadcast_message = response.text
    media = None
    caption = None

    if response.photo:
        media = response.photo.file_id  # Correct way to access the file_id of the photo
        caption = response.caption
    elif response.video:
        media = response.video.file_id
        caption = response.caption

    # Get all users from the database
    allusers = list(users.find())

    if not allusers:
        await m.reply("No users found in the database.")
        return

    lel = await m.reply_text("`⚡️ Starting broadcast...`")
    success_count = 0
    failed_count = 0
    deactivated = 0
    blocked = 0

    # Loop through all users
    for user in allusers:
        userid = user.get("user_id")
        if not userid:
            failed_count += 1
            continue

        first_name = user.get("first_name", "Unknown")
        last_name = user.get("last_name", "Unknown")

        try:
            if media:
                # If media is provided, send it with the caption
                if response.photo:
                    await app.send_photo(userid, media, caption=caption)
                elif response.video:
                    await app.send_video(userid, media, caption=caption)
            else:
                # Send only the message text if no media is provided
                await app.send_message(userid, broadcast_message)
            success_count += 1
            logging.info(f"Successfully sent to {first_name} {last_name} (ID: {userid})")
        except FloodWait as ex:
            print(f"FloodWait: Sleeping for {ex.value} seconds.")
            await asyncio.sleep(ex.value)
            try:
                # Retry sending the message after sleep
                if media:
                    if response.photo:
                        await app.send_photo(userid, media, caption=caption)
                    elif response.video:
                        await app.send_video(userid, media, caption=caption)
                else:
                    await app.send_message(userid, broadcast_message)
                success_count += 1
                logging.info(f"Successfully sent after wait to {first_name} {last_name} (ID: {userid})")
            except Exception as inner_ex:
                print(f"Error after FloodWait for user {userid}: {inner_ex}")
                failed_count += 1
                logging.error(f"Failed to send after wait to {first_name} {last_name} (ID: {userid}): {inner_ex}")
        except errors.InputUserDeactivated:
            print(f"User {userid} is deactivated.")
            deactivated += 1
            remove_user(userid)
            logging.info(f"Deactivated user removed: {first_name} {last_name} (ID: {userid})")
        except errors.UserIsBlocked:
            print(f"Bot is blocked by user {userid}.")
            blocked += 1
            logging.info(f"Blocked by user: {first_name} {last_name} (ID: {userid})")
        except Exception as e:
            print(f"Failed to send to user {userid}: {e}")
            failed_count += 1
            logging.error(f"Failed to send to {first_name} {last_name} (ID: {userid}): {e}")

    await lel.edit(f"""
✅ Successfully sent to `{success_count}` users.
❌ Failed to send to `{failed_count}` users.
👾 Blocked by `{blocked}` users.
👻 Found `{deactivated}` deactivated users.
""")

# Log file should now contain detailed information about each user.
print("Broadcast complete. Check the 'broadcast_log.txt' file for more details.")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Users List in File ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("usersall") & filters.user(cfg.SUDO))
async def users_all(_, m: Message):
    # Extract all users
    all_users_list = all_users()
    
    if not all_users_list:
        await m.reply("No users found in the database.")
        return

    # Create a file with all users information
    file_path = "all_users.txt"
    with open(file_path, "w") as f:
        f.write("User ID | First Name | Last Name\n")
        for user in all_users_list:
            first_name = user.get("first_name", "Unknown")
            last_name = user.get("last_name", "Unknown")
            user_id = user.get("user_id", "Unknown")
            f.write(f"{user_id} | {first_name} | {last_name}\n")
    
    # Send the file to the admin
    await m.reply_document(file_path)
    
    # Remove the file after sending
    os.remove(file_path)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Broadcast Forward ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("fcast") & filters.user(cfg.SUDO))
async def fcast(_, m: Message):
    if not m.reply_to_message:
        await m.reply("Please reply to a message to forward.")
        return
    allusers = users.find()
    lel = await m.reply_text("⚡️ Processing...")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0

    for usrs in allusers:
        userid = usrs["user_id"]
        try:
            await m.reply_to_message.forward(int(userid))
            success += 1
            logging.info(f"Successfully forwarded to {userid}")
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
            await m.reply_to_message.forward(int(userid))
        except errors.InputUserDeactivated:
            deactivated += 1
            remove_user(userid)
            logging.info(f"Deactivated user removed: {userid}")
        except errors.UserIsBlocked:
            blocked += 1
            logging.info(f"Blocked by user: {userid}")
        except Exception as e:
            print(f"Error with user {userid}: {e}")
            failed += 1
            logging.error(f"Failed to forward to {userid}: {e}")

    await lel.edit(f"✅ Successfully forwarded to {success} users.\n❌ Failed to {failed} users.\n👾 Blocked by {blocked} users.\n👻 Found {deactivated} deactivated users.")

print("I'm Alive Now!")
app.run()
