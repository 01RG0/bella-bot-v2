import { useState } from 'react';
import botAvatar from '../assets/bot-avatar.jpg';

interface LoginScreenProps {
  onLogin: (userData: { username: string; avatar: string }) => void;
}

export function LoginScreen({ onLogin }: LoginScreenProps) {
  const [isLoading, setIsLoading] = useState(false);

  const handleDiscordLogin = () => {
    setIsLoading(true);
    // Discord OAuth URL
    const clientId = import.meta.env.VITE_DISCORD_CLIENT_ID;
    const rawRedirect = import.meta.env.VITE_DISCORD_REDIRECT_URI;

    if (!clientId) {
      console.error('Missing VITE_DISCORD_CLIENT_ID environment variable');
      alert('Discord client ID is not configured. Please check your environment.');
      setIsLoading(false);
      return;
    }

    if (!rawRedirect) {
      console.error('Missing VITE_DISCORD_REDIRECT_URI environment variable');
      alert('Discord redirect URI is not configured. Please check your environment.');
      setIsLoading(false);
      return;
    }

    const redirectUri = encodeURIComponent(rawRedirect);
    const scope = encodeURIComponent('identify email');
    const discordAuthUrl = `https://discord.com/api/oauth2/authorize?client_id=${clientId}&redirect_uri=${redirectUri}&response_type=code&scope=${scope}`;
    
    // Redirect to Discord OAuth
    window.location.href = discordAuthUrl;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-neutral-900 via-neutral-800 to-neutral-900 flex items-center justify-center px-4 py-8">
      <div className="w-full max-w-md">
        <div className="text-center mb-6 sm:mb-8 animate-fade-in">
          <div className="inline-flex w-20 h-20 sm:w-24 sm:h-24 rounded-full items-center justify-center mb-4 sm:mb-6 shadow-2xl overflow-hidden ring-4 ring-white/10">
            <img src={botAvatar} alt="Bella Bot" className="w-full h-full object-cover" />
          </div>
          <h1 className="text-white text-3xl sm:text-4xl mb-2 sm:mb-3">Welcome to Bella</h1>
          <p className="text-neutral-400 text-base sm:text-lg">Your AI Assistant Dashboard</p>
        </div>

        <div className="bg-[rgb(39,39,39)] rounded-2xl p-6 sm:p-8 shadow-2xl transform transition-all hover:scale-[1.02]">
          <button
            onClick={handleDiscordLogin}
            disabled={isLoading}
            className="w-full flex items-center justify-center gap-3 bg-[#5865F2] text-white px-4 sm:px-6 py-3 sm:py-4 rounded-xl hover:bg-[#4752C4] transition-all shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed transform hover:-translate-y-0.5 text-sm sm:text-base"
          >
            {isLoading ? (
              <>
                <div className="w-5 h-5 sm:w-6 sm:h-6 border-2 border-white border-t-transparent rounded-full animate-spin" />
                <span>Connecting...</span>
              </>
            ) : (
              <>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" className="sm:w-6 sm:h-6">
                  <path d="M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515a.074.074 0 0 0-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 0 0-5.487 0a12.64 12.64 0 0 0-.617-1.25a.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 0 0 .031.057a19.9 19.9 0 0 0 5.993 3.03a.078.078 0 0 0 .084-.028a14.09 14.09 0 0 0 1.226-1.994a.076.076 0 0 0-.041-.106a13.107 13.107 0 0 1-1.872-.892a.077.077 0 0 1-.008-.128a10.2 10.2 0 0 0 .372-.292a.074.074 0 0 1 .077-.01c3.928 1.793 8.18 1.793 12.062 0a.074.074 0 0 1 .078.01c.12.098.246.198.373.292a.077.077 0 0 1-.006.127a12.299 12.299 0 0 1-1.873.892a.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028a19.839 19.839 0 0 0 6.002-3.03a.077.077 0 0 0 .032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 0 0-.031-.03zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419c0-1.333.956-2.419 2.157-2.419c1.21 0 2.176 1.096 2.157 2.42c0 1.333-.956 2.418-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419c0-1.333.955-2.419 2.157-2.419c1.21 0 2.176 1.096 2.157 2.42c0 1.333-.946 2.418-2.157 2.418z"/>
                </svg>
                <span>Continue with Discord</span>
              </>
            )}
          </button>

          <p className="text-neutral-500 text-xs sm:text-sm text-center mt-4 sm:mt-6">
            By logging in, you agree to Bella&apos;s Terms of Service
          </p>
        </div>

        <p className="text-neutral-500 text-xs sm:text-sm text-center mt-6 sm:mt-8">
          Need help? <span className="text-neutral-300 hover:text-white cursor-pointer transition-colors">Contact on discord trumy or r.g._</span>
        </p>
      </div>
    </div>
  );
}