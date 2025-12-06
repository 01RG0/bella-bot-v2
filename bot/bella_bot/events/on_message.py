import discord
import os
import asyncio
import httpx
from ..services.ai_service import AIService
from ..services.image_service import ImageService
from ..services.memory_service import MemoryService
from ..config import config

ai_service = AIService()
image_service = ImageService(
    default_model=config.IMAGE_MODEL,
    auth_token=config.POLLINATIONS_TOKEN
)
memory_service = MemoryService()


async def _post_event(payload: dict):
    # Send event to dashboard API if configured; fire-and-forget
    api_base = os.getenv('BOT_PUBLIC_URL') or os.getenv('VITE_API_BASE_URL') or 'http://localhost:8000'
    url = api_base.rstrip('/') + '/events'
    try:
        async with httpx.AsyncClient() as client:
            await client.post(url, json=payload, timeout=5)
    except Exception:
        # Don't let dashboard failures affect bot behavior
        pass


async def setup(bot):
    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        content = message.content.lower().strip()
        
        # 1. Detection Keywords
        bella_names = [
            'bella', 'bela',
            'بيلا', 'بللا', 'بلا'
        ]
        
        image_triggers = [
            # Verbs
            "generate", "create", "make", "draw", "imagine", "gen",
            "paint", "design", "سوي", "اصنع", "ارسم", "صمم", "اعمل", "صور",
            "رسم", "تخيل",
            # Nouns (Contextual triggers)
            "image", "picture", "art", "drawing", "photo", "pic", "صورة",
            "رسمة", "فن", "تصميم", "صوره",
            # Legacy/Specific
            "create image", "اصنعي صورة"
        ]

        # 2. Check Triggers
        is_bella_mentioned = any(name in content for name in bella_names)
        is_direct_mention = bot.user in message.mentions or content.startswith(f"<@{bot.user.id}>")
        
        should_respond = is_direct_mention or is_bella_mentioned
        
        # 3. Handle Response (if triggered and not a slash command)
        if should_respond and not content.startswith('/'):
            async with message.channel.typing():
                
                # Check for Image Generation Request
                is_image_request = any(trigger in content for trigger in image_triggers)
                
                if is_image_request:
                    # Clean up prompt: remove trigger words and bella names
                    prompt = message.content # Use original case for prompt
                    clean_content_lower = content
                    
                    # Remove mentions first
                    for mention in message.mentions:
                        prompt = prompt.replace(f"<@{mention.id}>", "").replace(f"<@!{mention.id}>", "")
                        clean_content_lower = clean_content_lower.replace(f"<@{mention.id}>", "").replace(f"<@!{mention.id}>", "")

                    # Remove keywords (simple remove)
                    for word in bella_names + image_triggers:
                        # Case insensitive remove logic could be complex, 
                        # but simplistic replace on lowercase check is hard on original string
                        # Let's just strip known triggers from the prompt roughly
                        if word in prompt.lower():
                             # This is a bit rough, but works for "Bella draw cat" -> " cat"
                             # proper regex replace ignoring case is better but keep it simple
                             import re
                             prompt = re.sub(re.escape(word), '', prompt, flags=re.IGNORECASE)
                    
                    prompt = prompt.strip()
                    if not prompt or len(prompt) < 2:
                        prompt = "artistic masterpiece" # Fallback
                        
                    try:
                        image_url = await image_service.generate_image(prompt)
                        
                        embed = discord.Embed(title="🎨 Here is your image!", color=discord.Color.purple())
                        embed.set_image(url=image_url)
                        embed.set_footer(text=f"Prompt: {prompt}")
                        await message.reply(embed=embed)
                        
                        asyncio.create_task(_post_event({
                            'type': 'image_generated',
                            'payload': {'author': str(message.author), 'prompt': prompt}
                        }))
                        return # Done
                    except Exception as e:
                        await message.reply(f"❌ I encountered an error generating that image.")
                        print(f"Image Gen Error: {e}")
                        return

                # Normal Chat Response
                clean_message = message.content
                for mention in message.mentions:
                    clean_message = clean_message.replace(f"<@{mention.id}>", "").replace(f"<@!{mention.id}>", "")
                
                # 1. Update User State & Get Memory
                user_roles = [r.name for r in message.author.roles] if hasattr(message.author, 'roles') else []
                await memory_service.update_user_interaction(str(message.author.id), str(message.author), user_roles)
                user_memory = await memory_service.get_memory(str(message.author.id))
                
                # 2. Build Context
                context_parts = [
                    f"User: {message.author.display_name} (ID: {message.author.id})",
                    f"Roles: {', '.join(user_roles) if user_roles else 'None'}"
                ]
                if user_memory.get("facts"):
                    context_parts.append("KNOWN FACTS:")
                    context_parts.extend([f"- {fact}" for fact in user_memory["facts"]])
                
                # 3. Resolve Prompt
                system_prompt = behavior_service.resolve_system_instruction(str(message.author.id), user_roles)
                
                # 4. Generate with Context & Prompt
                response, new_memories = await ai_service.generate_response(
                    clean_message, 
                    user_context="\n".join(context_parts),
                    system_instruction=system_prompt
                )
                
                # 5. Save New Memories
                for memory in new_memories:
                    await memory_service.add_memory_fact(str(message.author.id), memory)
                
                if len(response) > 2000:
                    chunks = [response[i:i+2000] for i in range(0, len(response), 2000)]
                    for chunk in chunks:
                        await message.reply(chunk)
                else:
                    await message.reply(response)

                # Notify dashboard
                asyncio.create_task(_post_event({
                    'type': 'mention_reply',
                    'payload': {
                        'author': str(message.author),
                        'channel': str(message.channel),
                        'content': clean_message,
                        'response': response[:2000]
                    }
                }))

        # Process commands
        await bot.process_commands(message)
