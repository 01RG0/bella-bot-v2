import discord
from ..services.ai_service import AIService

ai_service = AIService()

async def setup(bot):
    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return
        
        # Check if bot is mentioned or message starts with bot mention
        bot_mentioned = bot.user in message.mentions or message.content.startswith(f"<@{bot.user.id}>") or message.content.startswith(f"<@!{bot.user.id}>")
        
        # Auto-respond to mentions (excluding commands)
        if bot_mentioned and not message.content.startswith('/'):
            # Remove the mention from the message
            clean_message = message.content
            for mention in message.mentions:
                clean_message = clean_message.replace(f"<@{mention.id}>", "").replace(f"<@!{mention.id}>", "")
            clean_message = clean_message.strip()
            
            # If there's actual content after removing mentions, respond
            if clean_message:
                # Show typing indicator
                async with message.channel.typing():
                    response = await ai_service.generate_response(clean_message)
                    # Split long responses (Discord has 2000 char limit)
                    if len(response) > 2000:
                        chunks = [response[i:i+2000] for i in range(0, len(response), 2000)]
                        for chunk in chunks:
                            await message.reply(chunk)
                    else:
                        await message.reply(response)
        
        # Process commands
        await bot.process_commands(message)