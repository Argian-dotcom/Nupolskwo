
import os
import logging
import discord
from discord import app_commands

# ---------------- CONFIGURATION ----------------

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

logger = logging.getLogger("discord_bot")

# ---------------- BOT SETUP ----------------

intents = discord.Intents.default()
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)


@bot.event
async def on_ready():
    logger.info("Bot online: %s", bot.user)


@bot.event
async def setup_hook():
    synced = await tree.sync()
    logger.info("Synced %s slash commands", len(synced))


# ---------------- BOT COMMANDS ----------------

@tree.command(
    name="ping",
    description="Check whether the bot is online",
)
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"Pong! Latency: {round(bot.latency * 1000)} ms"
    )


@tree.command(
    name="serverinfo",
    description="Show information about this server",
)
@app_commands.guild_only()
async def serverinfo(interaction: discord.Interaction):
    guild = interaction.guild

    if guild is None:
        await interaction.response.send_message(
            "Use this command inside a server.",
            ephemeral=True,
        )
        return

    embed = discord.Embed(
        title=guild.name,
        description="Server information",
        color=discord.Color.red(),
    )
    embed.add_field(name="Server ID", value=str(guild.id))
    embed.add_field(name="Members", value=str(guild.member_count))
    embed.add_field(name="Text/Voice Channels", value=str(len(guild.channels)))

    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)

    await interaction.response.send_message(embed=embed)


@tree.command(
    name="channels",
    description="List this server's channels",
)
@app_commands.guild_only()
async def channels(interaction: discord.Interaction):
    guild = interaction.guild

    if guild is None:
        await interaction.response.send_message(
            "Use this command inside a server.",
            ephemeral=True,
        )
        return

    channel_names = [
        f"#{channel.name}"
        for channel in guild.channels
    ]

    if not channel_names:
        message = "No channels found."
    else:
        message = "\n".join(channel_names[:40])

        if len(channel_names) > 40:
            message += f"\n...and {len(channel_names) - 40} more"

    await interaction.response.send_message(
        message,
        ephemeral=True,
    )


# ---------------- MAIN FUNCTION ----------------

def main():
    if not TOKEN:
        raise RuntimeError(
            "Missing DISCORD_BOT_TOKEN environment variable."
        )

    logger.info("Starting Discord bot...")
    bot.run(TOKEN, log_handler=None)


if __name__ == "__main__":
    main()
