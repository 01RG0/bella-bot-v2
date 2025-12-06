# Deployment Guide

## Option 1: The "Simple" Monolith (Recommended for You)
**Use Render (Docker)** for EVERYTHING.
This runs the Website, the Bot, and the API in one single container. It is the easiest way to make Music, Auto-run, and everything work together.

1. **Platform**: Render (or Railway)
2. **Setup**: Connect your repo, use `Docker` environment.
3. **Result**: 
   - ✅ Music Works (Lavalink runs locally in docker)
   - ✅ Bot Works (Runs in background)
   - ✅ Web Works

---

## Option 2: The "Hybrid" (Vercel + External Bot)
Use this if you really want the website on Vercel.

### Part A: Vercel (Website & API)
1. Import repo to Vercel.
2. It will auto-detect `vercel.json`.
3. **Limitations**: The "Play Music" buttons on the web dashboard (if added later) might fail if the bot isn't running elsewhere.

### Part B: The Bot (MUST Run Elsewhere)
Vercel cannot run the bot process. You must run the bot on a **VPS**, **Render**, **Heroku**, or **Your PC**.

**If running on Render (Worker Mode):**
1. Create a "Background Worker" service on Render.
2. Command: `python -m bella_bot`
3. Environment: `DISCORD_TOKEN`, etc.

### Part C: Lavalink (Music Server)
The bot needs a Lavalink server to play music.
- **On Docker (Option 1)**: It's included automatically.
- **On Vercel (Option 2)**: IMPOSSIBLE. You must host Lavalink separately (e.g. on a cheap VPS) and set `LAVALINK_HOST` in your `.env`.

---

## ⚡ Summary
- **For a fully working Music Bot**: Use **Docker** (Render/Railway).
- **For just a Chat Bot & Dashboard**: Vercel is fine, but you still need to run the bot script somewhere.
