@app.on_message(filters.command("bcast") & filters.user(cfg.SUDO))
async def bcast(_, m: Message):
    # Check if the command has a message to broadcast
    if len(m.command) < 2:
        if not m.from_user.is_bot:  # Ensures the response isn't duplicated by bot replies
            await m.reply("Usage: `/bcast Your Message Here`", parse_mode=enums.ParseMode.MARKDOWN)
        return

    # Get the broadcast message
    broadcast_message = m.text.split(" ", 1)[1]
    allusers = list(users.find())

    if not allusers:
        await m.reply("No users found in the database.")
        return

    lel = await m.reply_text("`⚡️ Starting broadcast...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0

    for user in allusers:
        userid = user.get("user_id")
        if not userid:
            failed += 1
            continue

        try:
            # Send the broadcast message
            await app.send_message(chat_id=int(userid), text=broadcast_message)
            success += 1
        except FloodWait as ex:
            print(f"FloodWait: Sleeping for {ex.value} seconds.")
            await asyncio.sleep(ex.value)
            try:
                await app.send_message(chat_id=int(userid), text=broadcast_message)
                success += 1
            except Exception as inner_ex:
                print(f"Error after FloodWait for user {userid}: {inner_ex}")
                failed += 1
        except errors.InputUserDeactivated:
            print(f"User {userid} is deactivated.")
            deactivated += 1
            remove_user(userid)
        except errors.UserIsBlocked:
            print(f"Bot is blocked by user {userid}.")
            blocked += 1
        except Exception as e:
            print(f"Failed to send to user {userid}: {e}")
            failed += 1

    await lel.edit(f"""
✅ Successfully sent to `{success}` users.
❌ Failed to send to `{failed}` users.
👾 Blocked by `{blocked}` users.
👻 Found `{deactivated}` deactivated users.
""")
