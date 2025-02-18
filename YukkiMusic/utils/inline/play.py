#
# Copyright (C) 2024 by TheTeamVivek@Github, < https://github.com/TheTeamVivek >.
#
# This file is part of < https://github.com/TheTeamVivek/YukkiMusic > project,
# and is released under the MIT License.
# Please see < https://github.com/TheTeamVivek/YukkiMusic/blob/master/LICENSE >
#
# All rights reserved.
#
import math

from pyrogram.types import InlineKeyboardButton

from YukkiMusic.utils.formatters import time_to_seconds


def get_progress_bar(percentage):
    umm = math.floor(percentage)

    if 0 < umm <= 10:
        return "⬛️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️"
    elif 10 < umm <= 20:
        return "⬛️⬛️⬜️⬜️⬜️⬜️⬜️⬜️⬜️"
    elif 20 < umm <= 30:
        return "⬛️⬛️⬛️⬜️⬜️⬜️⬜️⬜️⬜️"
    elif 30 < umm <= 40:
        return "⬛️⬛️⬛️⬛️⬜️⬜️⬜️⬜️⬜️"
    elif 40 < umm <= 50:
        return "⬛️⬛️⬛️⬛️⬛️⬜️⬜️⬜️⬜️"
    elif 50 < umm <= 60:
        return "⬛️⬛️⬛️⬛️⬛️⬛️⬜️⬜️⬜️"
    elif 60 < umm <= 70:
        return "⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬜️⬜️"
    elif 70 < umm <= 80:
        return "⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬜️"
    elif 80 < umm <= 90:
        return "⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️"
    elif 90 < umm <= 100:
        return "⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️"
    else:
        return "⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️"


def stream_markup_timer(_, videoid, chat_id, played, dur):
    played_sec = time_to_seconds(played)
    duration_sec = time_to_seconds(dur)
    percentage = (played_sec / duration_sec) * 100

    bar = get_progress_bar(percentage)

    buttons = [
        [
            InlineKeyboardButton(
                text=f"{played} {bar} {dur}",
                callback_data="GetTimer",
            )
        ],
        [
            InlineKeyboardButton(
                text="🏛 𝐑𝐀𝐍𝐆𝐄𝐑",
                callback_data=f"MainMarkup {videoid}|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="⏮ 10 ثانیه",
                callback_data=f"ADMIN 1|{chat_id}",
            ),
            InlineKeyboardButton(
                text="⏭ 10 ثانیه",
                callback_data=f"ADMIN 2|{chat_id}",
            ),
            InlineKeyboardButton(
                text="⏮ 30 ثانیه",
                callback_data=f"ADMIN 3|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="🔇 بی صدا",
                callback_data=f"ADMIN Mute|{chat_id}",
            ),
            InlineKeyboardButton(
                text="🔊 با صدا",
                callback_data=f"ADMIN Unmute|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="🔉 کم کردن صدا",
                callback_data=f"ADMIN Volume -10|{chat_id}",
            ),
            InlineKeyboardButton(
                text="🔊 زیاد کردن صدا",
                callback_data=f"ADMIN Volume +10|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="⏸ مکث",
                callback_data=f"ADMIN Pause|{chat_id}",
            ),
            InlineKeyboardButton(
                text="▶️ ادامه",
                callback_data=f"ADMIN Resume|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="⏹ توقف",
                callback_data=f"ADMIN Stop|{chat_id}",
            ),
            InlineKeyboardButton(
                text="⏭ بعدی",
                callback_data=f"ADMIN Skip|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="📥 دانلود",
                callback_data=f"ADMIN Download|{videoid}|{chat_id}",
            ),
            InlineKeyboardButton(
                text="📝 پلی لیست",
                callback_data=f"ADMIN Playlist|{videoid}|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="◀️",
                callback_data=f"Pages Back|0|{videoid}|{chat_id}",
            ),
            InlineKeyboardButton(
                text="❌ بستن",
                callback_data="close",
            ),
            InlineKeyboardButton(
                text="▶️",
                callback_data=f"Pages Forw|0|{videoid}|{chat_id}",
            ),
        ],
    ]
    return buttons
def stream_markup(_, videoid, chat_id):
    buttons = [
        [
            InlineKeyboardButton(
                text=f"🏛 𝐑𝐀𝐍𝐆𝐄𝐑",
                callback_data=f"MainMarkup {videoid}|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="⏮ 10 ثانیه",
                callback_data=f"ADMIN 1|{chat_id}",
            ),
            InlineKeyboardButton(
                text="⏭ 10 ثانیه",
                callback_data=f"ADMIN 2|{chat_id}",
            ),
            InlineKeyboardButton(
                text="⏮ 30 ثانیه",
                callback_data=f"ADMIN 3|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="🔇 بی صدا",
                callback_data=f"ADMIN Mute|{chat_id}",
            ),
            InlineKeyboardButton(
                text="🔊 با صدا",
                callback_data=f"ADMIN Unmute|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="🔉 کم کردن صدا",
                callback_data=f"ADMIN Volume -10|{chat_id}",
            ),
            InlineKeyboardButton(
                text="🔊 زیاد کردن صدا",
                callback_data=f"ADMIN Volume +10|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="⏸ مکث",
                callback_data=f"ADMIN Pause|{chat_id}",
            ),
            InlineKeyboardButton(
                text="▶️ ادامه",
                callback_data=f"ADMIN Resume|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="⏹ توقف",
                callback_data=f"ADMIN Stop|{chat_id}",
            ),
            InlineKeyboardButton(
                text="⏭ بعدی",
                callback_data=f"ADMIN Skip|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="📥 دانلود",
                callback_data=f"ADMIN Download|{videoid}|{chat_id}",
            ),
            InlineKeyboardButton(
                text="📝 پلی لیست",
                callback_data=f"ADMIN Playlist|{videoid}|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="❌ بستن",
                callback_data="close",
            ),
        ],
    ]
    return buttons


def telegram_markup_timer(_, chat_id, played, dur):
    played_sec = time_to_seconds(played)
    duration_sec = time_to_seconds(dur)
    percentage = (played_sec / duration_sec) * 100

    bar = get_progress_bar(percentage)

    buttons = [
        [
            InlineKeyboardButton(
                text=f"{played} {bar} {dur}",
                callback_data="GetTimer",
            )
        ],
        [
            InlineKeyboardButton(
                text="🏛 𝐑𝐀𝐍𝐆𝐄𝐑",
                callback_data=f"MainMarkup None|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="⏮ 10 ثانیه",
                callback_data=f"ADMIN 1|{chat_id}",
            ),
            InlineKeyboardButton(
                text="⏭ 10 ثانیه",
                callback_data=f"ADMIN 2|{chat_id}",
            ),
            InlineKeyboardButton(
                text="⏮ 30 ثانیه",
                callback_data=f"ADMIN 3|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="🔇 بی صدا",
                callback_data=f"ADMIN Mute|{chat_id}",
            ),
            InlineKeyboardButton(
                text="🔊 با صدا",
                callback_data=f"ADMIN Unmute|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="🔉 کم کردن صدا",
                callback_data=f"ADMIN Volume -10|{chat_id}",
            ),
            InlineKeyboardButton(
                text="🔊 زیاد کردن صدا",
                callback_data=f"ADMIN Volume +10|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="⏸ مکث",
                callback_data=f"ADMIN Pause|{chat_id}",
            ),
            InlineKeyboardButton(
                text="▶️ ادامه",
                callback_data=f"ADMIN Resume|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="⏹ توقف",
                callback_data=f"ADMIN Stop|{chat_id}",
            ),
            InlineKeyboardButton(
                text="⏭ بعدی",
                callback_data=f"ADMIN Skip|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="📥 دانلود",
                callback_data=f"ADMIN Download|None|{chat_id}",
            ),
            InlineKeyboardButton(
                text="📝 پلی لیست",
                callback_data=f"ADMIN Playlist|None|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="❌ بستن",
                callback_data="close",
            ),
        ],
    ]
    return buttons
def telegram_markup(_, chat_id):
    buttons = [
        [
            InlineKeyboardButton(
                text="🏛 𝐑𝐀𝐍𝐆𝐄𝐑",
                callback_data=f"MainMarkup None|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="⏮ 10 ثانیه",
                callback_data=f"ADMIN 1|{chat_id}",
            ),
            InlineKeyboardButton(
                text="⏭ 10 ثانیه",
                callback_data=f"ADMIN 2|{chat_id}",
            ),
            InlineKeyboardButton(
                text="⏮ 30 ثانیه",
                callback_data=f"ADMIN 3|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="🔇 بی صدا",
                callback_data=f"ADMIN Mute|{chat_id}",
            ),
            InlineKeyboardButton(
                text="🔊 با صدا",
                callback_data=f"ADMIN Unmute|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="🔉 کم کردن صدا",
                callback_data=f"ADMIN Volume -10|{chat_id}",
            ),
            InlineKeyboardButton(
                text="🔊 زیاد کردن صدا",
                callback_data=f"ADMIN Volume +10|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="⏸ مکث",
                callback_data=f"ADMIN Pause|{chat_id}",
            ),
            InlineKeyboardButton(
                text="▶️ ادامه",
                callback_data=f"ADMIN Resume|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="⏹ توقف",
                callback_data=f"ADMIN Stop|{chat_id}",
            ),
            InlineKeyboardButton(
                text="⏭ بعدی",
                callback_data=f"ADMIN Skip|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="📥 دانلود",
                callback_data=f"ADMIN Download|None|{chat_id}",
            ),
            InlineKeyboardButton(
                text="📝 پلی لیست",
                callback_data=f"ADMIN Playlist|None|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="❌ بستن",
                callback_data="close",
            ),
        ],
    ]
    return buttons


def track_markup(_, videoid, user_id, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(
                text="🎵 پخش موزیک",
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text="🎥 پخش ویدیو",
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="❌ بستن",
                callback_data=f"forceclose {videoid}|{user_id}",
            ),
        ],
    ]
    return buttons


def playlist_markup(_, videoid, user_id, ptype, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(
                text="🎵 پخش موزیک",
                callback_data=f"YukkiPlaylists {videoid}|{user_id}|{ptype}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text="🎥 پخش ویدیو",
                callback_data=f"YukkiPlaylists {videoid}|{user_id}|{ptype}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="❌ بستن",
                callback_data=f"forceclose {videoid}|{user_id}",
            ),
        ],
    ]
    return buttons


def livestream_markup(_, videoid, user_id, mode, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(
                text="🎥 پخش زنده",
                callback_data=f"LiveStream {videoid}|{user_id}|{mode}|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="❌ بستن",
                callback_data=f"forceclose {videoid}|{user_id}",
            ),
        ],
    ]
    return buttons
def slider_markup(_, videoid, user_id, query, query_type, channel, fplay):
    query = f"{query[:20]}"
    buttons = [
        [
            InlineKeyboardButton(
                text="🎵 پخش موزیک",
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text="🎥 پخش ویدیو",
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="◀️",
                callback_data=f"slider B|{query_type}|{query}|{user_id}|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text="❌ بستن",
                callback_data=f"forceclose {query}|{user_id}",
            ),
            InlineKeyboardButton(
                text="▶️",
                callback_data=f"slider F|{query_type}|{query}|{user_id}|{channel}|{fplay}",
            ),
        ],
    ]
    return buttons


def panel_markup_1(_, videoid, chat_id):
    buttons = [
        [
            InlineKeyboardButton(
                text="⏮ 10 ثانیه",
                callback_data=f"ADMIN 1|{chat_id}",
            ),
            InlineKeyboardButton(
                text="⏭ 10 ثانیه",
                callback_data=f"ADMIN 2|{chat_id}",
            ),
            InlineKeyboardButton(
                text="⏮ 30 ثانیه",
                callback_data=f"ADMIN 3|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="🏛 𝐑𝐀𝐍𝐆𝐄𝐑",
                callback_data=f"MainMarkup {videoid}|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="🔇 بی صدا",
                callback_data=f"ADMIN Mute|{chat_id}",
            ),
            InlineKeyboardButton(
                text="🔊 با صدا",
                callback_data=f"ADMIN Unmute|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="🔉 کم کردن صدا",
                callback_data=f"ADMIN Volume -10|{chat_id}",
            ),
            InlineKeyboardButton(
                text="🔊 زیاد کردن صدا",
                callback_data=f"ADMIN Volume +10|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="⏸ مکث",
                callback_data=f"ADMIN Pause|{chat_id}",
            ),
            InlineKeyboardButton(
                text="▶️ ادامه",
                callback_data=f"ADMIN Resume|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="⏹ توقف",
                callback_data=f"ADMIN Stop|{chat_id}",
            ),
            InlineKeyboardButton(
                text="⏭ بعدی",
                callback_data=f"ADMIN Skip|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="📥 دانلود",
                callback_data=f"ADMIN Download|{videoid}|{chat_id}",
            ),
            InlineKeyboardButton(
                text="📝 پلی لیست",
                callback_data=f"ADMIN Playlist|{videoid}|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="◀️",
                callback_data=f"Pages Back|0|{videoid}|{chat_id}",
            ),
            InlineKeyboardButton(
                text="❌ بستن",
                callback_data="close",
            ),
            InlineKeyboardButton(
                text="▶️",
                callback_data=f"Pages Forw|0|{videoid}|{chat_id}",
            ),
        ],
    ]
    return buttons


def panel_markup_2(_, videoid, chat_id):
    buttons = [
        [
            InlineKeyboardButton(
                text="🔇 بی صدا",
                callback_data=f"ADMIN Mute|{chat_id}",
            ),
            InlineKeyboardButton(
                text="🔊 با صدا",
                callback_data=f"ADMIN Unmute|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="🔀 ترکیب",
                callback_data=f"ADMIN Shuffle|{chat_id}",
            ),
            InlineKeyboardButton(
                text="🔁 لوپ",
                callback_data=f"ADMIN Loop|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="◀️",
                callback_data=f"Pages Back|1|{videoid}|{chat_id}",
            ),
            InlineKeyboardButton(
                text="❌ بستن",
                callback_data="close",
            ),
            InlineKeyboardButton(
                text="▶️",
                callback_data=f"Pages Forw|1|{videoid}|{chat_id}",
            ),
        ],
    ]
    return buttons


def panel_markup_3(_, videoid, chat_id):
    buttons = [
        [
            InlineKeyboardButton(
                text="⏮ 10 ثانیه",
                callback_data=f"ADMIN 1|{chat_id}",
            ),
            InlineKeyboardButton(
                text="⏭ 10 ثانیه",
                callback_data=f"ADMIN 2|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="⏮ 30 ثانیه",
                callback_data=f"ADMIN 3|{chat_id}",
            ),
            InlineKeyboardButton(
                text="⏭ 30 ثانیه",
                callback_data=f"ADMIN 4|{chat_id}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="◀️",
                callback_data=f"Pages Back|2|{videoid}|{chat_id}",
            ),
            InlineKeyboardButton(
                text="❌ بستن",
                callback_data="close",
            ),
            InlineKeyboardButton(
                text="▶️",
                callback_data=f"Pages Forw|2|{videoid}|{chat_id}",
            ),
        ],
    ]
    return buttons            
