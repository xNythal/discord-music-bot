import discord
from discord.ext import commands
import utils
import constants
from discord import app_commands
import os
import asyncio
import math

class Bot(commands.Bot):
    async def close(self):
        utils.write_log("Bot is shutting down...", "INFO")
        utils.seperate_log()
        await super().close()

bot = Bot(intents=discord.Intents.all(), command_prefix=constants.COMMAND_PREFIX, help_command=None)

@bot.event
async def on_ready():
    await bot.change_presence(activity=constants.BOT_ACTIVITY)
    utils.write_log(f"Bot is online and ready! Logged in as {bot.user}", "INFO")

@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.MemberNotFound):
        return
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.reply(constants.cooldown_message(math.ceil(error.retry_after)), mention_author=False)
        return
    raise error

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    if message.content.startswith(f"{bot.command_prefix}developer") and not await bot.is_owner(message.author):
        return utils.write_log(f"'{message.author}' tried to use the developer command without owner permissions.", "WARN")
    await bot.process_commands(message)

@bot.hybrid_command(name="help", description="Show all commands or details for one.")
@commands.cooldown(1, 5, commands.BucketType.user)
async def help(ctx: commands.Context, query: str = None):
    embed = discord.Embed(color=discord.Color.blurple())
    query = query.lower() if query else None

    cmds = bot.tree.get_commands()

    if query:
        for cmd in cmds:
            if cmd.name.lower() == query:
                if isinstance(cmd, app_commands.Group):
                    embed.title = f"🌀 /{cmd.name}"
                    embed.description = cmd.description or "No description."
                    for sub in cmd.commands:
                        embed.add_field(
                            name=f"`/{cmd.name} {sub.name}`",
                            value=sub.description or "No description.",
                            inline=False
                        )
                else:
                    embed.title = f"📘 /{cmd.name}"
                    embed.description = cmd.description or "No description."
                break
        else:
            embed.title = "❓ Not Found"
            embed.description = f'No slash command or group named **"{query}"** was found.'
    else:
        embed.title = "📖 Help Menu"
        embed.description = "Command groups and individual commands:"
        groups: dict[str, list[str]] = {}

        for cmd in cmds:
            if isinstance(cmd, app_commands.Group):
                groups[f"🌀 {cmd.name.title()}"] = [
                    f"`/{cmd.name} {sub.name}` - {sub.description or 'No description'}"
                    for sub in cmd.commands if isinstance(sub, app_commands.Command)
                ]
            elif isinstance(cmd, app_commands.Command):
                groups.setdefault("📁 Miscellaneous", []).append(
                    f"`/{cmd.name}` - {cmd.description or 'No description'}"
                )

        for title, cmds in groups.items():
            embed.add_field(name=title, value="\n".join(cmds), inline=False)

        embed.set_footer(text="Use /<command> or $help <name> for details 🚀")

    await ctx.reply(embed=embed, mention_author=False)

@bot.hybrid_command(name="invite", description="Sends the bot's invite link.")
@commands.cooldown(1, 5, commands.BucketType.user)
async def invite(ctx: commands.Context):
    invite_link = discord.utils.oauth_url(client_id=bot.application_id, permissions=discord.Permissions(permissions=8))
    await ctx.reply(embed=constants.invite_embed(invite_link), mention_author=False)

if constants.SUPPORT_SERVER_URL:
    @bot.hybrid_command(name="support", description="Get support or join the support server.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def support(ctx: commands.Context):
        await ctx.reply(embed=constants.support_embed(), mention_author=False)

@bot.hybrid_command(description="Measure's the bot's latency in milliseconds.")
@commands.cooldown(1, 5, commands.BucketType.user)
async def ping(ctx: commands.Context):
    latency = round(bot.latency * 1000)
    await ctx.reply(embed=constants.ping_embed(latency), mention_author=False)

async def loadCogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
            await bot.load_extension(f"cogs.{filename[:-3]}")

asyncio.run(loadCogs())

if __name__ == "__main__":
    bot.run(constants.BOT_TOKEN)