import discord
from discord import app_commands
from ..services.ai_service import AIService

ai_service = AIService()

async def setup(bot):
    @bot.tree.command(name="chat", description="Chat with Bella (AI assistant)")
    async def chat(interaction: discord.Interaction, message: str):
        """Chat command that uses Gemini to generate responses"""
        await interaction.response.defer(thinking=True)
        
        try:
            response = await ai_service.generate_response(message)
            
            # Discord has a 2000 character limit per message
            if len(response) > 2000:
                # Split into chunks
                chunks = [response[i:i+2000] for i in range(0, len(response), 2000)]
                await interaction.followup.send(chunks[0])
                for chunk in chunks[1:]:
                    await interaction.followup.send(chunk)
            else:
                await interaction.followup.send(response)
        except Exception as e:
            await interaction.followup.send(f"Sorry, I encountered an error: {str(e)}")