import uvloop
uvloop.install()

import asyncio
import os
import importlib.util
import traceback
from datetime import datetime
from functools import wraps

from pyrogram import Client, StopPropagation, errors
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import (
    BotCommand,
    BotCommandScopeAllChatAdministrators,
    BotCommandScopeAllGroupChats,
    BotCommandScopeAllPrivateChats,
    BotCommandScopeChat,
    BotCommandScopeChatMember,
)
from pyrogram.errors import (
    FloodWait,
    MessageNotModified,
    MessageIdInvalid,
    ChatSendMediaForbidden,
    ChatSendPhotosForbidden,
    ChatWriteForbidden,
)
from pyrogram.handlers import MessageHandler

import config
from ..logging import LOGGER

class YukkiBot(Client):
    def __init__(self, *args, **kwargs):
        LOGGER(__name__).info("Starting Bot...")
        super().__init__(*args, **kwargs)
        self.loaded_plug_counts = 0

    async def log_message(self, message: str, error: bool = False):
        """Send log messages to bot owner and log group"""
        try:
            # ارسال به مالک در پیوی ربات
            for owner_id in config.OWNER_ID:
                try:
                    await self.send_message(owner_id, message)
                except Exception as e:
                    LOGGER(__name__).warning(f"Failed to send log to owner {owner_id}: {str(e)}")
            
            # اگر گروه لاگ تنظیم شده، به آنجا هم ارسال کن
            if hasattr(config, 'LOG_GROUP_ID') and config.LOG_GROUP_ID:
                try:
                    await self.send_message(config.LOG_GROUP_ID, message)
                except Exception as e:
                    LOGGER(__name__).warning(f"Failed to send log to log group: {str(e)}")
        except Exception as e:
            LOGGER(__name__).error(f"Failed to send logs: {str(e)}")
        
        # در هر صورت در کنسول هم لاگ کن
        if error:
            LOGGER(__name__).error(message)
        else:
            LOGGER(__name__).info(message)

    def on_message(self, filters=None, group=0):
        def decorator(func):
            @wraps(func)
            async def wrapper(client, message):
                try:
                    await func(client, message)
                except FloodWait as e:
                    await self.log_message(f"FloodWait: Sleeping for {e.value} seconds.")
                    await asyncio.sleep(e.value)
                except (
                    ChatWriteForbidden,
                    ChatSendMediaForbidden,
                    ChatSendPhotosForbidden,
                    MessageNotModified,
                    MessageIdInvalid,
                ):
                    pass
                except StopPropagation:
                    raise
                except Exception as e:
                    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    user_id = message.from_user.id if message.from_user else "Unknown"
                    chat_id = message.chat.id if message.chat else "Unknown"
                    chat_username = f"@{message.chat.username}" if message.chat and message.chat.username else "Private Group"
                    command = (
                        " ".join(message.command)
                        if hasattr(message, "command")
                        else message.text
                    )
                    error_trace = traceback.format_exc()
                    error_message = (
                        f"**❌ Bot Error Report**\n\n"
                        f"**Time:** {date_time}\n"
                        f"**Chat ID:** `{chat_id}`\n"
                        f"**Chat Username:** {chat_username}\n"
                        f"**User ID:** `{user_id}`\n"
                        f"**Command/Text:** `{command}`\n\n"
                        f"**Error Type:** `{type(e).__name__}`\n"
                        f"**Error Message:** `{str(e)}`\n\n"
                        f"**Traceback:**\n```{error_trace}```"
                    )
                    await self.log_message(error_message, error=True)

            handler = MessageHandler(wrapper, filters)
            self.add_handler(handler, group)
            return func

        return decorator

    async def start(self):
        await super().start()
        get_me = await self.get_me()
        self.username = get_me.username
        self.id = get_me.id
        self.name = f"{get_me.first_name} {get_me.last_name or ''}"
        self.mention = get_me.mention

        start_message = (
            f"🎵 **{self.mention} Bot Started**\n\n"
            f"🤖 **Bot ID:** `{self.id}`\n"
            f"📝 **Name:** {self.name}\n"
            f"👤 **Username:** @{self.username}"
        )
        
        await self.log_message(start_message)

        if config.SET_CMDS == str(True):
            try:
                await self._set_default_commands()
                await self.log_message("✅ Bot commands have been set successfully!")
            except Exception as e:
                await self.log_message(f"❌ Failed to set commands: {str(e)}", error=True)

        try:
            if hasattr(config, 'LOG_GROUP_ID') and config.LOG_GROUP_ID:
                member = await self.get_chat_member(config.LOG_GROUP_ID, "me")
                if member.status != ChatMemberStatus.ADMINISTRATOR:
                    await self.log_message("⚠️ Bot is not admin in logger group. Some features might not work properly.")
        except Exception as e:
            await self.log_message(f"⚠️ Couldn't check admin status in log group: {str(e)}")

        LOGGER(__name__).info(f"✨ MusicBot started as {self.name}")

    async def _set_default_commands(self):
        private_commands = [
            BotCommand("start", "Start the bot"),
            BotCommand("help", "Get help menu"),
            BotCommand("ping", "Check bot's latency"),
        ]
        group_commands = [BotCommand("play", "Play requested song")]
        admin_commands = [
            BotCommand("play", "Play requested song"),
            BotCommand("skip", "Skip current song"),
            BotCommand("pause", "Pause current song"),
            BotCommand("resume", "Resume paused song"),
            BotCommand("end", "End playback"),
            BotCommand("shuffle", "Shuffle queue"),
            BotCommand("playmode", "Change playmode"),
            BotCommand("settings", "Open settings"),
        ]
        owner_commands = [
            BotCommand("update", "Update bot"),
            BotCommand("restart", "Restart bot"),
            BotCommand("logs", "Get logs"),
            BotCommand("export", "Export database"),
            BotCommand("import", "Import database"),
            BotCommand("addsudo", "Add sudo user"),
            BotCommand("delsudo", "Remove sudo user"),
            BotCommand("sudolist", "List sudo users"),
            BotCommand("getvar", "Get config var"),
            BotCommand("delvar", "Delete config var"),
            BotCommand("setvar", "Set config var"),
            BotCommand("usage", "Get usage info"),
            BotCommand("maintenance", "Toggle maintenance"),
            BotCommand("logger", "Toggle logging"),
            BotCommand("block", "Block user"),
            BotCommand("unblock", "Unblock user"),
            BotCommand("blacklist", "Blacklist chat"),
            BotCommand("whitelist", "Whitelist chat"),
            BotCommand("blacklisted", "List blacklisted"),
            BotCommand("autoend", "Toggle auto-end"),
        ]

        try:
            await self.set_bot_commands(private_commands, scope=BotCommandScopeAllPrivateChats())
            await self.set_bot_commands(group_commands, scope=BotCommandScopeAllGroupChats())
            await self.set_bot_commands(admin_commands, scope=BotCommandScopeAllChatAdministrators())
            
            for owner_id in config.OWNER_ID:
                try:
                    await self.set_bot_commands(
                        owner_commands,
                        scope=BotCommandScopeChat(chat_id=owner_id)
                    )
                except Exception as e:
                    await self.log_message(f"Failed to set owner commands for {owner_id}: {str(e)}", error=True)
                    
        except Exception as e:
            await self.log_message(f"Failed to set commands: {str(e)}", error=True)

    def load_plugin(self, file_path: str, base_dir: str, utils=None):
        file_name = os.path.basename(file_path)
        module_name, ext = os.path.splitext(file_name)
        if module_name.startswith("__") or ext != ".py":
            return None

        relative_path = os.path.relpath(file_path, base_dir).replace(os.sep, ".")
        module_path = f"{os.path.basename(base_dir)}.{relative_path[:-3]}"

        try:
            spec = importlib.util.spec_from_file_location(module_path, file_path)
            module = importlib.util.module_from_spec(spec)
            module.logger = LOGGER(module_path)
            module.app = self
            module.Config = config

            if utils:
                module.utils = utils

            spec.loader.exec_module(module)
            self.loaded_plug_counts += 1
            LOGGER(__name__).info(f"✅ Loaded plugin: {module_path}")
            return module
            
        except Exception as e:
            LOGGER(__name__).error(f"❌ Failed to load {module_path}: {str(e)}")
            return None

    def load_plugins_from(self, base_folder: str):
        base_dir = os.path.abspath(base_folder)
        utils_path = os.path.join(base_dir, "utils.py")
        utils = None

        if os.path.exists(utils_path) and os.path.isfile(utils_path):
            try:
                spec = importlib.util.spec_from_file_location("utils", utils_path)
                utils = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(utils)
                LOGGER(__name__).info("✅ Loaded utils module")
            except Exception as e:
                LOGGER(__name__).error(f"❌ Failed to load utils module: {str(e)}")

        loaded_plugins = []
        for root, _, files in os.walk(base_dir):
            for file in files:
                if file.endswith(".py") and not file == "utils.py":
                    file_path = os.path.join(root, file)
                    mod = self.load_plugin(file_path, base_dir, utils)
                    if mod:
                        loaded_plugins.append(mod)

        return loaded_plugins

    async def run_shell_command(self, command: list):
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await process.communicate()

        return {
            "returncode": process.returncode,
            "stdout": stdout.decode().strip() if stdout else None,
            "stderr": stderr.decode().strip() if stderr else None,
        }
