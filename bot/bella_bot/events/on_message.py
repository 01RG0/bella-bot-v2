import discord

async def setup(bot):
    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return
        # Process message
        await bot.process_commands(message)