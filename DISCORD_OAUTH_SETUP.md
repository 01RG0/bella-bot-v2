# Discord OAuth Configuration Steps

## Your Current Settings
- **Client ID:** 1316758560398377020
- **Client Secret:** 4E6gsnoDi-UFDtvkRLN8nJ_TvJh0dhNW
- **Redirect URI:** http://localhost:5173/auth/discord/callback

## ⚠️ IMPORTANT: Update Discord Developer Portal

You need to add the redirect URI to your Discord application:

### Steps:

1. **Go to Discord Developer Portal**
   - https://discord.com/developers/applications

2. **Select Your Application**
   - Click on your app (should have your bot name)

3. **Go to OAuth2 > General**
   - URL: https://discord.com/developers/applications/1316758560398377020/oauth2/general

4. **Add Redirect URLs**
   - Click "Add Redirect" button
   - Add: `http://localhost:5173/auth/discord/callback`
   - Make sure to click "Save Changes"

5. **Verify Scopes**
   - Go to "OAuth2 > URL Generator"
   - Select Scopes: `identify`, `email`
   - You should see the callback URI listed

### After Setting Up:

1. **Verify .env has correct values:**
   ```
   VITE_DISCORD_CLIENT_ID=1316758560398377020
   VITE_DISCORD_CLIENT_SECRET=4E6gsnoDi-UFDtvkRLN8nJ_TvJh0dhNW
   VITE_DISCORD_REDIRECT_URI=http://localhost:5173/auth/discord/callback
   ```

2. **Restart the services:**
   ```powershell
   .\scripts\stop_all.ps1
   .\scripts\setup_and_run.ps1
   ```

3. **Test Login:**
   - Open http://localhost:5173 (dashboard)
   - Click "Continue with Discord"
   - You should be redirected to Discord login
   - After auth, you should see your user info in the dashboard

## Troubleshooting

**"Authentication Error"?**
- ❌ Redirect URI not added to Discord app — add it in Developer Portal
- ❌ Client ID/Secret mismatch — verify they're the same in .env and Discord Portal
- ❌ Services not restarted — restart API, bot, and frontend after updating .env

**"Discord client ID is not configured"?**
- Check VITE_DISCORD_CLIENT_ID is set in .env (not empty)
- Restart frontend: `npm run dev` in web/

**"Redirecting to login..." (infinite loop)?**
- Usually means redirect URI mismatch
- Verify http://localhost:5173/auth/discord/callback is in Discord Portal
- No trailing slash, exact match required

## Next Steps

1. Add the redirect URI to Discord Developer Portal (**do this first**)
2. Restart all services: `.\scripts\stop_all.ps1` then `.\scripts\setup_and_run.ps1`
3. Open http://localhost:5173 and test login
