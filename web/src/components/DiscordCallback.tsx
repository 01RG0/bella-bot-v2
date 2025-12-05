import { useEffect, useState } from 'react';
import { Bot } from 'lucide-react';

interface DiscordCallbackProps {
  onLogin: (userData: { username: string; avatar: string }) => void;
}

export function DiscordCallback({ onLogin }: DiscordCallbackProps) {
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const handleCallback = async () => {
      // Get the authorization code from URL
      const urlParams = new URLSearchParams(window.location.search);
      const code = urlParams.get('code');
      const errorParam = urlParams.get('error');

      if (errorParam) {
        setError('Authentication cancelled or failed');
        // Redirect back to login after 3 seconds
        setTimeout(() => {
          window.location.href = '/';
        }, 3000);
        return;
      }

      if (!code) {
        setError('No authorization code received');
        setTimeout(() => {
          window.location.href = '/';
        }, 3000);
        return;
      }

      try {
        // Exchange code for access token
        const tokenResponse = await fetch('https://discord.com/api/oauth2/token', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: new URLSearchParams({
            client_id: import.meta.env.VITE_DISCORD_CLIENT_ID,
            client_secret: import.meta.env.VITE_DISCORD_CLIENT_SECRET,
            grant_type: 'authorization_code',
            code: code,
            redirect_uri: import.meta.env.VITE_DISCORD_REDIRECT_URI,
          }),
        });

        if (!tokenResponse.ok) {
          throw new Error('Failed to exchange code for token');
        }

        const tokenData = await tokenResponse.json();

        // Get user information
        const userResponse = await fetch('https://discord.com/api/users/@me', {
          headers: {
            Authorization: `Bearer ${tokenData.access_token}`,
          },
        });

        if (!userResponse.ok) {
          throw new Error('Failed to fetch user data');
        }

        const userData = await userResponse.json();

        // Login with user data
        onLogin({
          username: `${userData.username}#${userData.discriminator !== '0' ? userData.discriminator : userData.username}`,
          avatar: userData.avatar 
            ? `https://cdn.discordapp.com/avatars/${userData.id}/${userData.avatar}.png`
            : 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400&h=400&fit=crop',
        });

      } catch (err) {
        console.error('Discord OAuth error:', err);
        setError('Failed to authenticate with Discord. Please try again.');
        setTimeout(() => {
          window.location.href = '/';
        }, 3000);
      }
    };

    handleCallback();
  }, [onLogin]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-neutral-900 via-neutral-800 to-neutral-900 flex items-center justify-center px-4 py-8">
      <div className="w-full max-w-md text-center">
        <div className="inline-flex w-16 h-16 sm:w-20 sm:h-20 bg-gradient-to-br from-white to-neutral-100 rounded-2xl sm:rounded-3xl items-center justify-center mb-4 sm:mb-6 shadow-2xl">
          <Bot className="w-10 h-10 sm:w-12 sm:h-12 text-neutral-900" />
        </div>
        
        {error ? (
          <div className="bg-red-500/10 border border-red-500/20 rounded-xl p-6 sm:p-8">
            <h2 className="text-red-400 text-xl sm:text-2xl mb-2">Authentication Error</h2>
            <p className="text-red-300 text-sm sm:text-base">{error}</p>
            <p className="text-neutral-500 text-xs sm:text-sm mt-4">Redirecting to login...</p>
          </div>
        ) : (
          <div className="bg-[rgb(39,39,39)] rounded-xl p-6 sm:p-8">
            <div className="w-12 h-12 sm:w-16 sm:h-16 border-4 border-[#5865F2] border-t-transparent rounded-full animate-spin mx-auto mb-4" />
            <h2 className="text-white text-xl sm:text-2xl mb-2">Authenticating...</h2>
            <p className="text-neutral-400 text-sm sm:text-base">Connecting with Discord</p>
          </div>
        )}
      </div>
    </div>
  );
}