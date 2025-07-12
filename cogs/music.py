from discord.ext import commands
from discord import app_commands
import discord
import utils
import constants
import asyncio
import yt_dlp

class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        with open(constants.DJ_ROLES_FILE, "r") as f:
            self.dj_roles = [int(role.strip()) for role in f.readlines() if role.strip().isdigit()]

    @commands.hybrid_command(name="play", description="Play music from a YouTube link or search query.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def play(self, ctx: commands.Context, *, query: str):
        if not utils.has_djrole(ctx.author, self.dj_roles):
            return await ctx.reply(constants.DJROLE_MISSING_MESSAGE, mention_author=False)

        if not ctx.author.voice or not ctx.author.voice.channel:
            return await ctx.reply("🔇 You must be in a voice channel to play music.", mention_author=False)

        # Voice connection logic
        vc = ctx.guild.voice_client
        if vc is None or not vc.is_connected():
            vc = await ctx.author.voice.channel.connect()
        elif ctx.author.voice.channel != vc.channel:
            await vc.disconnect(force=True)
            vc = await ctx.author.voice.channel.connect()

        # Determine if input is URL or query
        ytdlp_opts = {
            'format': 'bestaudio',
            'quiet': True,
            'default_search': 'ytsearch',
        }

        try:
            with yt_dlp.YoutubeDL(ytdlp_opts) as ydl:
                extraction_input = query if utils.is_url(query) else f"ytsearch:{query}"
                info = ydl.extract_info(extraction_input, download=False)

                # Handle flat search results
                if 'entries' in info and isinstance(info['entries'], list):
                    info = info['entries'][0]

                stream_url = info['url']
                title = info.get('title', 'Unknown Track')

        except Exception as e:
            return await ctx.reply(f"❌ Failed to extract audio: `{e}`", mention_author=False)

        def after_playing(error):
            try:
                if error:
                    print(f"Error occurred while playing audio: {error}")
                else:
                    vc.play(discord.FFmpegPCMAudio(stream_url), after=after_playing)
            except discord.ClientException as e:
                if e.args[0] == "Not connected to voice.":
                    return

        if vc.is_playing():
            await vc.disconnect()
            vc = await ctx.author.voice.channel.connect()
        asyncio.create_task(utils.monitor_idle(vc, constants.IDLE_TIMEOUT_MINUTES))
        vc.play(discord.FFmpegPCMAudio(stream_url), after=after_playing)
        await ctx.reply(f"🎶 Now playing: **{title}**", mention_author=False)

    @commands.hybrid_command(name="stop", description="Disconnect the bot from the voice channel.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def stop(self, ctx: commands.Context):
        if not utils.has_djrole(ctx.author, self.dj_roles):
            return await ctx.reply("🚫 You don't have permission to use this command.", mention_author=False)

        vc = ctx.guild.voice_client
        if not vc or not vc.is_connected():
            return await ctx.reply("🤷 I'm not connected to any voice channel.", mention_author=False)

        await vc.disconnect()
        await ctx.reply(constants.STOP_MESSAGE, mention_author=False)

    @commands.hybrid_command(name="add-dj", description="Add or remove DJ roles for music commands.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    @app_commands.default_permissions(manage_roles=True)
    async def add_dj(self, ctx: commands.Context, role: discord.Role):
        if not ctx.author.guild_permissions.manage_roles:
            return await ctx.reply("🚫 You don't have permission to manage roles.", mention_author=False)
        if role in ctx.guild.roles:
            if role.id not in self.dj_roles:
                self.dj_roles.append(role.id)
                with open(constants.DJ_ROLES_FILE, "a") as file:
                    file.write(f"{role.id}\n")
                await ctx.reply(f"✅ {role.mention} has been added as a DJ role.", mention_author=False)
            else:
                await ctx.reply(f"❌ {role.mention} is already a DJ role.", mention_author=False)
    
    @commands.hybrid_command(name="del-dj", description="Add or remove DJ roles for music commands.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    @app_commands.default_permissions(manage_roles=True)
    async def del_dj(self, ctx: commands.Context, role: discord.Role):
        if not ctx.author.guild_permissions.manage_roles:
            return await ctx.reply("🚫 You don't have permission to manage roles.", mention_author=False)
        if role in ctx.guild.roles:
            if role.id in self.dj_roles:
                self.dj_roles.remove(role.id)
                with open(constants.DJ_ROLES_FILE, "w") as file:
                    file.writelines([f"{role_id}\n" for role_id in self.dj_roles])
                await ctx.reply(f"✅ {role.mention} has been removed as a DJ role.", mention_author=False)
            else:
                await ctx.reply(f"❌ {role} is not a DJ role.", mention_author=False)
        else:
            await ctx.reply(f"❌ {role} is not a valid role.", mention_author=False)
    
    @commands.hybrid_command(name="djroles", description="View all DJ roles for this server.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def djroles(self, ctx: commands.Context):
        role_mentions = [
            f"- {ctx.guild.get_role(role_id).mention}"
            for role_id in self.dj_roles
            if ctx.guild.get_role(role_id)
        ]

        if not role_mentions:
            return await ctx.reply("ℹ️ No DJ roles have been set for this server yet.", mention_author=False)

        response = "**🎧 DJ Roles for this server:**\n" + "\n".join(role_mentions)
        await ctx.reply(response, mention_author=False)

    @commands.hybrid_command(name="pause", description="Pause the current track.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pause(self, ctx: commands.Context):
        if not utils.has_djrole(ctx.author, self.dj_roles):
            return await ctx.reply("🚫 You don't have permission to use this command.", mention_author=False)

        vc = ctx.guild.voice_client
        if not vc or not vc.is_connected():
            return await ctx.reply("🤷 I'm not connected to any voice channel.", mention_author=False)
        if not vc.is_playing():
            return await ctx.reply("🛑 Nothing is currently playing.", mention_author=False)

        vc.pause()
        await ctx.reply(constants.PAUSE_MESSAGE, mention_author=False)
    
    @commands.hybrid_command(name="resume", description="Resume paused music.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def resume(self, ctx: commands.Context):
        if not utils.has_djrole(ctx.author, self.dj_roles):
            return await ctx.reply("🚫 You don't have permission to use this command.", mention_author=False)

        vc = ctx.guild.voice_client
        if not vc or not vc.is_connected():
            return await ctx.reply("🤷 I'm not connected to any voice channel.", mention_author=False)
        if not vc.is_paused():
            return await ctx.reply("🟢 Music isn't paused right now.", mention_author=False)

        vc.resume()
        await ctx.reply(constants.RESUME_MESSAGE, mention_author=False)



async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))
