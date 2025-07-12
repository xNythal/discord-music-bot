import discord
from .config import SUPPORT_SERVER_URL

# Static Reply Texts
RESUME_MESSAGE = "▶️ Resumed playback."
PAUSE_MESSAGE = "⏸️ Paused playback."
STOP_MESSAGE = "🛑 Disconnected from the voice channel."
DJROLE_MISSING_MESSAGE = "🚫 You don't have permission to use this command."

# Dynamic Reply Builders
def ping_embed(latency: int) -> discord.Embed:
    return discord.Embed(title="🏓 Pong!", color=discord.Color.green()).add_field(name="Latency:", value=f"{latency}ms")

def cooldown_message(retry_after: int) -> str:
    return f"⏳ This command is on cooldown. Try again in {retry_after} seconds."

def support_embed() -> discord.Embed:
    return (
        discord.Embed(
            title="🛠️ Support",
            description=f"If you need help or want to report an issue, join our [Support Server]({SUPPORT_SERVER_URL}).",
            color=discord.Color.green()
        )
        .set_footer(text="We're here to help 🤝")
    )

def invite_embed(invite_link) -> discord.Embed:
    return (
        discord.Embed(
            title="🔗 Invite Me!",
            description=f"Want to add me to your server? Just click [here]({invite_link})!",
            color=discord.Color.red()
        )
        .set_footer(text="Thank you for choosing our bot ❤️")
    )