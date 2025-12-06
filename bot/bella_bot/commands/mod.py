import discord
from discord import app_commands
from discord.ext import commands
import datetime

class ModerationCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="kick", description="Kick a member from the server")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        if member.top_role >= interaction.user.top_role and interaction.user.id != interaction.guild.owner_id:
             await interaction.response.send_message("❌ You cannot kick this user due to role hierarchy.", ephemeral=True)
             return
             
        await member.kick(reason=reason)
        await interaction.response.send_message(f"👢 **{member}** has been kicked. Reason: {reason or 'None'}")

    @app_commands.command(name="ban", description="Ban a member from the server")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        if member.top_role >= interaction.user.top_role and interaction.user.id != interaction.guild.owner_id:
             await interaction.response.send_message("❌ You cannot ban this user due to role hierarchy.", ephemeral=True)
             return

        await member.ban(reason=reason)
        await interaction.response.send_message(f"🔨 **{member}** has been banned. Reason: {reason or 'None'}")

    @app_commands.command(name="unban", description="Unban a user by ID")
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, user_id: str, reason: str = None):
        try:
            user = await self.bot.fetch_user(int(user_id))
            await interaction.guild.unban(user, reason=reason)
            await interaction.response.send_message(f"🔓 **{user}** has been unbanned.")
        except discord.NotFound:
            await interaction.response.send_message("❌ User not found.", ephemeral=True)
        except ValueError:
            await interaction.response.send_message("❌ Invalid User ID.", ephemeral=True)

    @app_commands.command(name="timeout", description="Timeout a member")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def timeout(self, interaction: discord.Interaction, member: discord.Member, minutes: int, reason: str = None):
        if member.top_role >= interaction.user.top_role and interaction.user.id != interaction.guild.owner_id:
             await interaction.response.send_message("❌ You cannot timeout this user.", ephemeral=True)
             return

        duration = datetime.timedelta(minutes=minutes)
        await member.timeout(duration, reason=reason)
        await interaction.response.send_message(f"⏰ **{member}** has been timed out for {minutes} minutes.")

    @app_commands.command(name="untimeout", description="Remove timeout from a member")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def untimeout(self, interaction: discord.Interaction, member: discord.Member):
        await member.timeout(None)
        await interaction.response.send_message(f"🔓 Timeout removed from **{member}**.")

    @app_commands.command(name="mute", description="Server mute a member in voice channels")
    @app_commands.checks.has_permissions(mute_members=True)
    async def mute(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        if not member.voice:
            await interaction.response.send_message("❌ User is not in a voice channel.", ephemeral=True)
            return
        
        await member.edit(mute=True, reason=reason)
        await interaction.response.send_message(f"🔇 **{member}** has been server muted.")

    @app_commands.command(name="unmute", description="Unmute a member in voice channels")
    @app_commands.checks.has_permissions(mute_members=True)
    async def unmute(self, interaction: discord.Interaction, member: discord.Member):
        await member.edit(mute=False)
        await interaction.response.send_message(f"🔊 **{member}** has been unmuted.")

    @app_commands.command(name="deafen", description="Server deafen a member in voice channels")
    @app_commands.checks.has_permissions(deafen_members=True)
    async def deafen(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        if not member.voice:
            await interaction.response.send_message("❌ User is not in a voice channel.", ephemeral=True)
            return

        await member.edit(deafen=True, reason=reason)
        await interaction.response.send_message(f"🙉 **{member}** has been server deafened.")

    @app_commands.command(name="undeafen", description="Undeafen a member")
    @app_commands.checks.has_permissions(deafen_members=True)
    async def undeafen(self, interaction: discord.Interaction, member: discord.Member):
        await member.edit(deafen=False)
        await interaction.response.send_message(f"👂 **{member}** has been undeafened.")

async def setup(bot):
    await bot.add_cog(ModerationCommands(bot))