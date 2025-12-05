import discord
from discord import app_commands

async def setup(bot):
    @bot.tree.command(name="ban", description="Ban a user")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(interaction: discord.Interaction, user: discord.Member, reason: str = "No reason provided"):
        await user.ban(reason=reason)
        await interaction.response.send_message(f"Banned {user.mention} for: {reason}")

    @bot.tree.command(name="kick", description="Kick a user")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(interaction: discord.Interaction, user: discord.Member, reason: str = "No reason provided"):
        await user.kick(reason=reason)
        await interaction.response.send_message(f"Kicked {user.mention} for: {reason}")