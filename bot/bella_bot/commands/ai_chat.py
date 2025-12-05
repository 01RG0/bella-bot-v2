import discord
from discord import app_commands
from ..services.ai_service import AIService

ai_service = AIService()

async def setup(bot):
    @bot.tree.command(name="chat", description="Chat with AI")
    async def chat(interaction: discord.Interaction, message: str):
        response = await ai_service.generate_response(message)
        await interaction.response.send_message(response)