import datetime
import shutil
import time
from pathlib import Path

import discord
import psutil
from discord.ext import commands, tasks
from uitils.config import get_cog_config, ConfigError

DEFAULT_INTERVAL = 30
BAR_LENGTH = 12


def make_bar(percent):
    percent = max(0.0, min(100.0, percent))
    filled = round(percent / 100 * BAR_LENGTH)
    block = "🟩" if percent < 70 else "🟨" if percent < 90 else "🟥"
    return block * filled + "⬛" * (BAR_LENGTH - filled)


def format_bytes(value):
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if value < 1024 or unit == "TB":
            return f"{value:.1f} {unit}"
        value /= 1024


def format_duration(seconds):
    days, rem = divmod(int(seconds), 86400)
    hours, rem = divmod(rem, 3600)
    minutes, secs = divmod(rem, 60)
    parts = [f"{days}d"] if days else []
    return " ".join(parts + [f"{hours}h", f"{minutes}m", f"{secs}s"])


class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = None
        self.update_interval = DEFAULT_INTERVAL
        self.modules = {}
        self.message_id = None
        self.enabled = False
        self.embed_color = None
        self.started = time.time()
        psutil.cpu_percent(interval=None)

        try:
            config = get_cog_config("status")
        except ConfigError as e:
            print(f"[Status] Config error: {e}")
            return

        self.channel_id = config.get("channel_id")
        self.modules = config.get("modules") or {}
        embed_color = config.get("embed_color")
        if embed_color is not None:
            try:
                self.embed_color = int(str(embed_color).lstrip("#"), 16) & 0xFFFFFF
            except ValueError:
                print(f"[Status] Invalid 'embed_color' ({embed_color!r}), expected hex like '#ADD8E6'. Using default.")

        interval = config.get("update_interval")
        if isinstance(interval, (int, float)) and not isinstance(interval, bool) and interval > 0:
            self.update_interval = interval
        else:
            print(f"[Status] Invalid 'update_interval' ({interval!r}), using {DEFAULT_INTERVAL}s.")

        if not isinstance(self.channel_id, int) or isinstance(self.channel_id, bool):
            print("[Status] 'channel_id' is not set or not a number in config.json. Status updates disabled.")
            return
        if not isinstance(self.modules, dict) or not any(self.modules.values()):
            print("[Status] No status modules are active. Status updates disabled.")
            return

        self.enabled = True
        self.update_status.change_interval(seconds=self.update_interval)
        print("[Status] Status config loaded successfully.")

    def cog_unload(self):
        self.update_status.cancel()

    @commands.Cog.listener()
    async def on_ready(self):
        if self.enabled and not self.update_status.is_running():
            self.update_status.start()

    def build_container(self):
        def active(name):
            return bool(self.modules.get(name))

        colour = self.embed_color if self.embed_color is not None else 0x57F287
        items = [discord.ui.TextDisplay("## 📊 Bot Status"), discord.ui.Separator()]

        if active("uptime"):
            items.append(discord.ui.TextDisplay(f"⏱️ **Uptime**\n`{format_duration(time.time() - self.started)}`"))
        if active("ping"):
            items.append(discord.ui.TextDisplay(f"🏓 **Ping**\n`{round(self.bot.latency * 1000)} ms`"))

        if any(active(m) for m in ("memory", "cpu", "disk")):
            items.append(discord.ui.Separator())
        if active("memory"):
            mem = psutil.virtual_memory()
            items.append(discord.ui.TextDisplay(
                f"🧠 **Memory** — {mem.percent:.0f}%\n{make_bar(mem.percent)}\n"
                f"`{format_bytes(mem.used)} / {format_bytes(mem.total)}`"
            ))
        if active("cpu"):
            cpu = psutil.cpu_percent(interval=None)
            items.append(discord.ui.TextDisplay(
                f"⚙️ **CPU** — {cpu:.0f}%\n{make_bar(cpu)}\n`{psutil.cpu_count()} Threads`"
            ))
        if active("disk"):
            disk = shutil.disk_usage(Path.cwd().anchor or "/")
            percent = disk.used / disk.total * 100
            items.append(discord.ui.TextDisplay(
                f"💾 **Disk** — {percent:.0f}%\n{make_bar(percent)}\n"
                f"`{format_bytes(disk.used)} / {format_bytes(disk.total)}`"
            ))

        if active("network"):
            net = psutil.net_io_counters()
            items.append(discord.ui.Separator())
            items.append(discord.ui.TextDisplay(
                f"🌐 **Network**\n⬆️ `{format_bytes(net.bytes_sent)}`  ⬇️ `{format_bytes(net.bytes_recv)}`"
            ))

        items.append(discord.ui.Separator())
        items.append(discord.ui.TextDisplay(f"-# Updated <t:{int(time.time())}:R> • every {self.update_interval}s"))
        return discord.ui.Container(*items, colour=colour)
    
    @tasks.loop(seconds=DEFAULT_INTERVAL)
    async def update_status(self):
        channel = self.bot.get_channel(self.channel_id)
        if channel is None:
            print(f"[Status] Channel {self.channel_id} not found. Check 'channel_id' and the bot's access.")
            return

        try:
            message = None
            if self.message_id is not None:
                try:
                    message = await channel.fetch_message(self.message_id)
                except discord.NotFound:
                    print(f"[Status] Message {self.message_id} no longer exists, creating a new one.")
            view = discord.ui.DesignerView(self.build_container(), timeout=None, store=False)
            if message is None:
                await channel.purge(limit=5)
                message = await channel.send(view=view)
                self.message_id = message.id
            else:
                await message.edit(view=view)
        except discord.Forbidden:
            print(f"[Status] Missing permissions to read/send/edit messages in channel {self.channel_id}.")
        except discord.HTTPException as e:
            print(f"[Status] Discord API error while updating status (HTTP {e.status}): {e.text}")


def setup(bot):
    bot.add_cog(Status(bot))



