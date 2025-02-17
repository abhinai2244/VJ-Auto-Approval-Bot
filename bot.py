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
    response = await app.listen(m.chat.id, timeout=300)

    if response.text.lower() == "cancel":
        await prompt_message.edit("Broadcast cancelled.")
        return

    broadcast_message = response.text
    allusers = list(users.find())

    if not allusers:
        await m.reply("No users found in the database.")
        return

    lel = await m.reply_text("`⚡️ Starting broadcast...`")
    success_count = 0
    failed_count = 0
    deactivated = 0
    blocked = 0

    for user in allusers:
        userid = user.get("user_id")
        if not userid:
            failed_count += 1
            continue

        try:
            if response.photo:
                await app.send_photo(userid, response.photo[-1].file_id, caption=response.caption)
            elif response.video:
                await app.send_video(userid, response.video.file_id, caption=response.caption)
            else:
                await app.send_message(userid, broadcast_message)
            success_count += 1
        except FloodWait as ex:
            print(f"FloodWait: Sleeping for {ex.value} seconds.")
            await asyncio.sleep(ex.value)
            try:
                await app.send_message(chat_id=int(userid), text=broadcast_message)
                success_count += 1
            except Exception as inner_ex:
                print(f"Error after FloodWait for user {userid}: {inner_ex}")
                failed_count += 1
        except errors.InputUserDeactivated:
            print(f"User {userid} is deactivated.")
            deactivated += 1
            remove_user(userid)
        except errors.UserIsBlocked:
            print(f"Bot is blocked by user {userid}.")
            blocked += 1
        except Exception as e:
            print(f"Failed to send to user {userid}: {e}")
            failed_count += 1

    await lel.edit(f"""
✅ Successfully sent to `{success_count}` users.
❌ Failed to send to `{failed_count}` users.
👾 Blocked by `{blocked}` users.
👻 Found `{deactivated}` deactivated users.
""")
