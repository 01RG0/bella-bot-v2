import discord
from discord import app_commands
from discord.ext import commands
import wavelink
from typing import cast
from ..config import config

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        """Connect to Lavalink nodes when the cog loads."""
        nodes = [
            wavelink.Node(
                uri=f"{'https' if config.LAVALINK_SECURE else 'http'}://{config.LAVALINK_HOST}:{config.LAVALINK_PORT}",
                password=config.LAVALINK_PASSWORD
            )
        ]
        # Wavelink 3.x uses Pool.connect
        try:
           # Attempt connection but don't block/crash if it fails immediately (e.g. invalid host)
           # The bot should still run without music.
           await wavelink.Pool.connect(nodes=nodes, client=self.bot, cache_capacity=100)
        except Exception as e:
           print(f"Failed to connect to Lavalink: {e}")
           print("Music commands will not work until Lavalink is available.")

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, payload: wavelink.NodeReadyEventPayload):
        print(f"Lavalink Node connected: {payload.node.identifier}")

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, payload: wavelink.TrackEndEventPayload):
        """Auto-play next song in queue"""
        player = payload.player
        if not player: return
        
        if not player.queue.is_empty:
            next_track = player.queue.get()
            await player.play(next_track)
        else:
            # Optional: Disconnect after timeout or just stay
            pass

    @app_commands.command(name="join", description="Join your voice channel")
    async def join(self, interaction: discord.Interaction):
        if not interaction.user.voice:
            return await interaction.response.send_message("You are not in a voice channel!", ephemeral=True)
        
        channel = interaction.user.voice.channel
        if not interaction.guild.voice_client:
            await channel.connect(cls=wavelink.Player)
            await interaction.response.send_message(f"Joined {channel.name}")
        else:
            await interaction.response.send_message("I am already in a channel.", ephemeral=True)

    @app_commands.command(name="play", description="Play a song from YouTube or SoundCloud")
    async def play(self, interaction: discord.Interaction, search: str):
        if not interaction.user.voice:
            return await interaction.response.send_message("Join a channel first!", ephemeral=True)

        if not interaction.guild.voice_client:
            player: wavelink.Player = await interaction.user.voice.channel.connect(cls=wavelink.Player)
        else:
            player: wavelink.Player = cast(wavelink.Player, interaction.guild.voice_client)

        await interaction.response.defer()

        # Search for tracks
        try:
            tracks: wavelink.Search = await wavelink.Playable.search(search)
        except Exception as e:
            return await interaction.followup.send(f"Error searching: {e}")

        if not tracks:
            return await interaction.followup.send("No tracks found.")

        # Determine if playlist or single track
        if isinstance(tracks, wavelink.Playlist):
            for track in tracks.tracks:
                await player.queue.put_wait(track)
            response = f"Added playlist **{tracks.name}** ({len(tracks.tracks)} songs) to queue."
        else:
            track = tracks[0]
            await player.queue.put_wait(track)
            response = f"Added **{track.title}** to queue."

        if not player.playing:
            # Start playing if idle
            await player.play(player.queue.get())
            # Override response if it was just one track starting now
            if not isinstance(tracks, wavelink.Playlist):
                response = f"Playing **{track.title}**"

        await interaction.followup.send(response)

    @app_commands.command(name="skip", description="Skip current song")
    async def skip(self, interaction: discord.Interaction):
        player: wavelink.Player = cast(wavelink.Player, interaction.guild.voice_client)
        if not player or not player.playing:
            return await interaction.response.send_message("Not playing anything.", ephemeral=True)
        
        await player.skip(force=True)
        await interaction.response.send_message("Skipped!")

    @app_commands.command(name="stop", description="Stop music and clear queue")
    async def stop(self, interaction: discord.Interaction):
        player: wavelink.Player = cast(wavelink.Player, interaction.guild.voice_client)
        if not player: return await interaction.response.send_message("Not playing.", ephemeral=True)
        
        player.queue.clear()
        await player.stop()
        await interaction.response.send_message("Stopped and cleared queue.")

    @app_commands.command(name="pause", description="Pause/Resume music")
    async def pause(self, interaction: discord.Interaction):
        player: wavelink.Player = cast(wavelink.Player, interaction.guild.voice_client)
        if not player: return await interaction.response.send_message("Not playing.", ephemeral=True)
        
        await player.pause(not player.paused)
        status = "Paused" if player.paused else "Resumed"
        await interaction.response.send_message(f"{status} music.")

    @app_commands.command(name="volume", description="Set volume (0-100)")
    async def volume(self, interaction: discord.Interaction, value: int):
        player: wavelink.Player = cast(wavelink.Player, interaction.guild.voice_client)
        if not player: return await interaction.response.send_message("Not playing.", ephemeral=True)
        
        vol = max(0, min(100, value))
        await player.set_volume(vol)
        await interaction.response.send_message(f"Volume set to {vol}%")

    @app_commands.command(name="leave", description="Leave voice channel")
    async def leave(self, interaction: discord.Interaction):
        player: wavelink.Player = cast(wavelink.Player, interaction.guild.voice_client)
        if player:
            await player.disconnect()
            await interaction.response.send_message("Disconnected.")
        else:
            await interaction.response.send_message("Not connected.")

    @app_commands.command(name="queue", description="Show current queue")
    async def queue(self, interaction: discord.Interaction):
        player: wavelink.Player = cast(wavelink.Player, interaction.guild.voice_client)
        if not player or player.queue.is_empty:
            return await interaction.response.send_message("Queue is empty.", ephemeral=True)
        
        embed = discord.Embed(title="Music Queue", color=discord.Color.blue())
        queue_text = ""
        # Access queue history or upcoming? Usually queue is upcoming.
        for i, track in enumerate(player.queue):
            queue_text += f"{i+1}. {track.title} ({track.author})\n"
            if i >= 9: # Limit display
                queue_text += f"...and {len(player.queue) - 10} more"
                break
        
        embed.description = queue_text
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="nowplaying", description="Show playing song")
    async def nowplaying(self, interaction: discord.Interaction):
        player: wavelink.Player = cast(wavelink.Player, interaction.guild.voice_client)
        if not player or not player.current:
            return await interaction.response.send_message("Not playing.", ephemeral=True)
            
        track = player.current
        embed = discord.Embed(title=f"▶️ {track.title}", description=f"By: {track.author}", color=discord.Color.green())
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Music(bot))