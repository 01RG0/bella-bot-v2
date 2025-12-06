# Deployment Guide

## Option 1: The "Simple" Monolith (Recommended for You)
**Use Render (Docker)** for EVERYTHING.
This runs the Website, the Bot, and the API in one single container. It is the easiest way to make Music, Auto-run, and everything work together.

## Option 2: Pure Vercel (Web + "Serverless" Bot)
**If you MUST use Vercel for everything:**

1. **Dashboard & API**:
   - Import to Vercel.
   - Add Config: `DISCORD_TOKEN`, `MONGO_URI`, `GOOGLE_API_KEY`, `VITE_...` vars.
   - Add `DISCORD_PUBLIC_KEY` (Get this from Discord Developer Portal).

2. **The "Bot" (Interactions Mode)**:
   - In Discord Developer Portal -> **Interaction Endpoint URL**.
   - Set URL to: `https://your-vercel-app.vercel.app/api/interactions`
   - ✅ Slash commands like `/chat` will work.
   - ❌ **Music will NOT work** (requires persistent server).
   - ❌ **Listening to regular messages will NOT work** (requires Gateway).
   
This allows the "Bot" to technically respond to commands on Vercel, but with severe limitations compared to the Docker version.

## Option 3: The "Hybrid" (Best of Both Worlds)
- **Vercel**: Hosts the **Dashboard** and **API**.
- **Render/Railway**: Hosts the **Bot** (Python script) + **Lavalink**.
- This gives you the speed of Vercel for the web and the power of a real bot server for music.
