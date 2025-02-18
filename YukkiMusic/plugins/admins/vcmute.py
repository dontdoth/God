#
# Copyright (C) 2024 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/YukkiMusic > project,
# and is released under the MIT License.
# Please see < https://github.com/TheTeamVivek/YukkiMusic/blob/master/LICENSE >
#
# All rights reserved.
#

from pyrogram import filters
from pyrogram.types import Message

from strings import command

from config import BANNED_USERS
from YukkiMusic import app
from YukkiMusic.core.call import Yukki
from YukkiMusic.utils.database import (
    is_muted, mute_off, mute_on,
    get_volume, set_volume
)
from YukkiMusic.utils.decorators import AdminRightsCheck


@app.on_message(command("MUTE_COMMAND") & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def mute_admin(cli, message: Message, _, chat_id):
    if not len(message.command) == 1 or message.reply_to_message:
        return
    if await is_muted(chat_id):
        return await message.reply_text(_["admin_5"], disable_web_page_preview=True)
    await mute_on(chat_id)
    await Yukki.mute_stream(chat_id)
    await message.reply_text(
        _["admin_6"].format(message.from_user.mention), disable_web_page_preview=True
    )


@app.on_message(command("UNMUTE_COMMAND") & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def unmute_admin(Client, message: Message, _, chat_id):
    if not len(message.command) == 1 or message.reply_to_message:
        return
    if not await is_muted(chat_id):
        return await message.reply_text(_["admin_7"], disable_web_page_preview=True)
    await mute_off(chat_id)
    await Yukki.unmute_stream(chat_id)
    await message.reply_text(
        _["admin_8"].format(message.from_user.mention), disable_web_page_preview=True
    )


@app.on_message(command("VOLUME_COMMAND") & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def volume_control(client, message: Message, _, chat_id):
    if not len(message.command) == 2:
        current_volume = await get_volume(chat_id)
        return await message.reply_text(
            _["admin_35"].format(current_volume), disable_web_page_preview=True
        )
    
    try:
        volume = int(message.command[1])
    except ValueError:
        return await message.reply_text(
            _["admin_36"], disable_web_page_preview=True
        )
        
    if volume < 1 or volume > 200:
        return await message.reply_text(
            _["admin_37"], disable_web_page_preview=True
        )
        
    await set_volume(chat_id, volume)
    await Yukki.set_stream_volume(chat_id, volume)
    await message.reply_text(
        _["admin_38"].format(message.from_user.mention, volume),
        disable_web_page_preview=True
    )
