from discord.ext import commands
import utils as utils
import os
import random
import constants

async def update_status(bot):
    await bot.change_presence(activity=random.choice(constants.STATUS_LIST(bot)))

class Developer(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.group()
    async def developer(self, ctx):
        return
    @developer.command()
    async def serverlist(self, ctx):
        result = ""
        for server in self.bot.guilds:
            result += f"{server.name}\n"
        await ctx.reply(result, mention_author=False)
        utils.write_log(f"Sent the server list to '{ctx.author}'", "INFO")

    @developer.command()
    async def servercount(self, ctx):
        await ctx.reply(f"Bot is in {len(self.bot.guilds)} servers.")
        utils.write_log(f"Checked server count for '{ctx.author}'.", "INFO")

    @developer.command()
    async def sync(self, ctx):
        await self.bot.tree.sync()
        await ctx.reply("Synced the commands!", mention_author=False)
        utils.write_log(f"Commands synced successfully by '{ctx.author}'.", "INFO")

    @developer.command()
    async def restart(self, ctx):
        utils.write_log(f"'{ctx.author}' restarted the bot.", "INFO")
        await ctx.reply("Restarting bot...", mention_author=False)
        await self.bot.close()
        os.system("python main.py")

    @developer.command()
    async def stop(self, ctx):
        utils.write_log(f"'{ctx.author}' stopped the bot.", "INFO")
        await ctx.reply("Stopping bot...", mention_author=False)
        await self.bot.close()
    
    @developer.command()
    async def cls(self, ctx):
        os.system("cls" if os.name == "nt" else "clear")
        await ctx.reply("Console cleared!", mention_author=False)
        utils.write_log(f"'{ctx.author}' cleared the console.", "INFO")

    @developer.command()
    async def logs(self, ctx):
        with open(constants.LOG_FILE_PATH, "r") as f:
            log_content = f.read()
        log_parts = [log_content[i:i+1994] for i in range(0, len(log_content), 1994)]
        for part in log_parts:
            if part.strip():
                await ctx.send(f"```{part}```", mention_author=False)
        utils.write_log(f"Sent logs file to '{ctx.author}'.", "INFO")

    @developer.command()
    async def logsize(self, ctx):
        log_size = os.path.getsize(constants.LOG_FILE_PATH)
        await ctx.reply(f"Log file size: {log_size / 1024 / 1024:.2f} MBs", mention_author=False)
        utils.write_log(f"Checked log file size for '{ctx.author}'.", "INFO")

    @developer.command()
    async def clearlog(self, ctx):
        with open(constants.LOG_FILE_PATH, "w") as f:
            f.truncate(0)
        await ctx.reply("Log file cleared!", mention_author=False)
        utils.write_log(f"Log file was cleared by '{ctx.author}'.", "INFO")

async def setup(bot):
    await bot.add_cog(Developer(bot))