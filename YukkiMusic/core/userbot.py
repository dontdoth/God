import asyncio
import sys
import traceback
from datetime import datetime
from functools import wraps

from pyrogram import Client, StopPropagation
from pyrogram.errors import (
    FloodWait,
    MessageNotModified,
    MessageIdInvalid,
    ChatSendMediaForbidden,
    ChatSendPhotosForbidden,
    ChatWriteForbidden,
    PeerIdInvalid,
)
from pyrogram.handlers import MessageHandler
import config

from ..logging import LOGGER

assistants = []
assistantids = []


class Userbot(Client):
    def __init__(self):
        self.clients = []
        self.handlers = []

    def add(self, *args, **kwargs):
        """Add a new client to the Userbot."""
        self.clients.append(Client(*args, **kwargs))

    async def _start(self, client, index):
        LOGGER(__name__).info(f"Starting Assistant Client {index}")
        try:
            await client.start()
            assistants.append(index)
            
            try:
                get_me = await client.get_me()
                client.username = get_me.username
                client.id = get_me.id
                client.mention = get_me.mention
                assistantids.append(get_me.id)
                client.name = f"{get_me.first_name} {get_me.last_name or ''}".strip()

                # اضافه کردن هندلرهای ذخیره شده به کلاینت
                for handler, group in self.handlers:
                    client.add_handler(handler, group)

                # تلاش برای ارسال پیام به گروه لاگ
                if hasattr(config, 'LOG_GROUP_ID') and config.LOG_GROUP_ID:
                    try:
                        await client.send_message(
                            config.LOG_GROUP_ID,
                            f"🎵 Assistant {index} Started\n\n"
                            f"🤖 ID: `{client.id}`\n"
                            f"👤 Name: {client.name}\n"
                            f"📝 Username: @{client.username}"
                        )
                    except ChatWriteForbidden:
                        try:
                            await client.join_chat(config.LOG_GROUP_ID)
                            await client.send_message(
                                config.LOG_GROUP_ID,
                                f"🎵 Assistant {index} Started\n\n"
                                f"🤖 ID: `{client.id}`\n"
                                f"👤 Name: {client.name}\n"
                                f"📝 Username: @{client.username}"
                            )
                        except Exception as e:
                            LOGGER(__name__).warning(
                                f"Assistant {index} couldn't send message to log group: {str(e)}"
                            )
                    except PeerIdInvalid:
                        LOGGER(__name__).warning(
                            f"Assistant {index} couldn't find the log group. Please add the assistant to the group first."
                        )
                    except Exception as e:
                        LOGGER(__name__).warning(
                            f"Assistant {index} encountered an error while sending to log group: {str(e)}"
                        )

                # ارسال پیام به مالک در پیوی
                if hasattr(config, 'OWNER_ID'):
                    for owner_id in config.OWNER_ID:
                        try:
                            await client.send_message(
                                owner_id,
                                f"🎵 Assistant {index} Started\n\n"
                                f"🤖 ID: `{client.id}`\n"
                                f"👤 Name: {client.name}\n"
                                f"📝 Username: @{client.username}"
                            )
                        except Exception as e:
                            LOGGER(__name__).warning(
                                f"Assistant {index} couldn't send message to owner {owner_id}: {str(e)}"
                            )

            except Exception as e:
                LOGGER(__name__).error(
                    f"Error getting Assistant {index} info: {str(e)}"
                )
                return False

            LOGGER(__name__).info(f"Assistant {index} Started Successfully!")
            return True

        except Exception as e:
            LOGGER(__name__).error(
                f"Assistant Account {index} failed to start: {str(e)}"
            )
            return False

    async def start(self):
        """Start all clients."""
        results = []
        for i, client in enumerate(self.clients, start=1):
            result = await self._start(client, i)
            results.append(result)

        # اگر حداقل یک اسیستنت با موفقیت شروع شده باشد، ادامه میدهیم
        if any(results):
            LOGGER(__name__).info(
                f"Successfully started {sum(results)} out of {len(results)} assistants"
            )
        else:
            LOGGER(__name__).error("No assistants could be started. Please check your configuration.")

    async def stop(self):
        """Gracefully stop all clients."""
        for client in self.clients:
            try:
                await client.stop()
            except Exception as e:
                LOGGER(__name__).error(f"Error stopping client: {str(e)}")

    def on_message(self, filters=None, group=0):
        """Decorator for handling messages with error handling."""
        def decorator(func):
            @wraps(func)
            async def wrapper(client, message):
                try:
                    await func(client, message)
                except FloodWait as e:
                    LOGGER(__name__).warning(f"FloodWait: Sleeping for {e.value} seconds.")
                    await asyncio.sleep(e.value)
                except (
                    ChatWriteForbidden,
                    ChatSendMediaForbidden,
                    ChatSendPhotosForbidden,
                    MessageNotModified,
                    MessageIdInvalid,
                    PeerIdInvalid,
                ):
                    pass
                except StopPropagation:
                    raise
                except Exception as e:
                    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    user_id = message.from_user.id if message.from_user else "Unknown"
                    chat_id = message.chat.id if message.chat else "Unknown"
                    chat_username = (
                        f"@{message.chat.username}"
                        if message.chat and message.chat.username
                        else "Private Group"
                    )
                    command = (
                        " ".join(message.command)
                        if hasattr(message, "command")
                        else message.text
                    )
                    error_trace = traceback.format_exc()
                    error_message = (
                        f"**❌ Assistant Error Report**\n\n"
                        f"**⏰ Time:** {date_time}\n"
                        f"**💭 Chat ID:** `{chat_id}`\n"
                        f"**📝 Chat Username:** {chat_username}\n"
                        f"**👤 User ID:** `{user_id}`\n"
                        f"**💬 Command/Text:** `{command}`\n\n"
                        f"**❌ Error Type:** `{type(e).__name__}`\n"
                        f"**❌ Error Message:** `{str(e)}`\n\n"
                        f"**🔍 Traceback:**\n```{error_trace}```"
                    )
                    
                    # تلاش برای ارسال خطا به گروه لاگ
                    if hasattr(config, 'LOG_GROUP_ID'):
                        try:
                            await client.send_message(config.LOG_GROUP_ID, error_message)
                        except Exception:
                            pass
                    
                    # تلاش برای ارسال خطا به مالک
                    if hasattr(config, 'OWNER_ID'):
                        for owner_id in config.OWNER_ID:
                            try:
                                await client.send_message(owner_id, error_message)
                            except Exception:
                                pass

                    LOGGER(__name__).error(
                        f"Error in message handler: {str(e)}\n{error_trace}"
                    )

            handler = MessageHandler(wrapper, filters)
            self.handlers.append((handler, group))
            return func

        return decorator
