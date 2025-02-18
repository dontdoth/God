import os
import re
import asyncio
from typing import Union, Tuple
from async_lru import alru_cache
from yt_dlp import YoutubeDL
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message
from youtubesearchpython.__future__ import VideosSearch

import config
from YukkiMusic.utils.database import is_on_off
from YukkiMusic.utils.formatters import seconds_to_min, time_to_seconds

class YouTube:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"
        self.status = "https://www.youtube.com/oembed?url="
        self.listbase = "https://youtube.com/playlist?list="
        self.reg = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

    @alru_cache(maxsize=None)
    async def exists(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if re.search(self.regex, link):
            return True
        return False

    @alru_cache(maxsize=None)
    async def url(self, message_1: Message) -> Union[str, None]:
        messages = [message_1]
        if message_1.reply_to_message:
            messages.append(message_1.reply_to_message)
        text = ""
        offset = None
        length = None
        for message in messages:
            if offset:
                break
            if message.entities:
                for entity in message.entities:
                    if entity.type == MessageEntityType.URL:
                        text = message.text or message.caption
                        offset, length = entity.offset, entity.length
                        break
            elif message.caption_entities:
                for entity in message.caption_entities:
                    if entity.type == MessageEntityType.TEXT_LINK:
                        return entity.url
        if offset in (None,):
            return None
        return text[offset : offset + length]

    @alru_cache(maxsize=None)
    async def details(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            title = result["title"]
            duration_min = result["duration"]
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            vidid = result["id"]
            if str(duration_min) == "None":
                duration_sec = 0
            else:
                duration_sec = int(time_to_seconds(duration_min))
        return title, duration_min, duration_sec, thumbnail, vidid

    @alru_cache(maxsize=None)
    async def title(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            title = result["title"]
        return title

    @alru_cache(maxsize=None)
    async def duration(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            duration = result["duration"]
        return duration

    @alru_cache(maxsize=None)
    async def thumbnail(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        return thumbnail

    async def video(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        proc = await asyncio.create_subprocess_exec(
            "yt-dlp",
            "-g",
            "-f",
            "best[height<=?720][width<=?1280]",
            f"{link}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        if stdout:
            return 1, stdout.decode().split("\n")[0]
        return 0, stderr.decode()

    @alru_cache(maxsize=None)
    async def playlist(self, link, limit, videoid: Union[bool, str] = None):
        if videoid:
            link = self.listbase + link
        if "&" in link:
            link = link.split("&")[0]
        playlist = []
        try:
            info = await self._get_playlist_info(link, limit)
            for track in info['entries'][:limit]:
                playlist.append(track['id'])
            return playlist
        except Exception as e:
            print(f"Playlist error: {e}")
            return []

    async def _get_playlist_info(self, url: str, limit: int):
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
            'playlist_items': f'1-{limit}'
        }
        with YoutubeDL(ydl_opts) as ydl:
            return await asyncio.get_event_loop().run_in_executor(
                None, ydl.extract_info, url, False
            )

    @alru_cache(maxsize=None)
    async def track(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            title = result["title"]
            duration_min = result["duration"]
            vidid = result["id"]
            yturl = result["link"]
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        track_details = {
            "title": title,
            "link": yturl,
            "vidid": vidid,
            "duration_min": duration_min,
            "thumb": thumbnail
        }
        return track_details, vidid

    async def download(
        self,
        link: str,
        mystic,
        video: Union[bool, str] = None,
        videoid: Union[bool, str] = None,
        songaudio: Union[bool, str] = None,
        songvideo: Union[bool, str] = None,
        format_id: Union[bool, str] = None,
        title: Union[bool, str] = None,
    ) -> Tuple[str, bool]:
        """Download video/audio from YouTube link."""
        
        if not os.path.exists("downloads"):
            os.makedirs("downloads")
            
        if videoid:
            link = self.base + link

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": f"downloads/{title or '%(id)s'}.%(ext)s",
            "geo_bypass": True,
            "nocheckcertificate": True,
            "quiet": True,
            "no_warnings": True,
            "prefer_ffmpeg": True,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        }

        if video:
            ydl_opts.update({
                "format": "best",
                "postprocessors": []
            })

        elif songvideo:
            ydl_opts.update({
                "format": format_id,
                "postprocessors": []
            })

        try:
            with YoutubeDL(ydl_opts) as ydl:
                try:
                    info = ydl.extract_info(link, download=True)
                    filepath = ydl.prepare_filename(info)
                    if not os.path.exists(filepath):
                        filepath = filepath.rsplit(".", 1)[0] + ".mp3"
                    
                    if not os.path.exists(filepath):
                        await mystic.edit_text("❌ Download failed")
                        return None, None
                        
                    return filepath, True
                    
                except Exception as e:
                    print(f"Download error: {e}")
                    await mystic.edit_text(f"❌ Error: {str(e)}")
                    return None, None
                    
        except Exception as e:
            print(f"YoutubeDL error: {e}")
            await mystic.edit_text("❌ Download failed")
            return None, None

    @alru_cache(maxsize=None)
    async def slider(
        self,
        link: str, 
        query_type: int,
        videoid: Union[bool, str] = None,
    ):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=10)
        for result in (await results.next())["result"]:
            title = result["title"]
            duration_min = result["duration"]
            vidid = result["id"] 
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        return title, duration_min, thumbnail, vidid
