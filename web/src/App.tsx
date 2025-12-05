import { useState } from 'react';
import { LoginScreen } from './components/LoginScreen';
import { DiscordCallback } from './components/DiscordCallback';
import { Header } from './components/Header';
import { StatsCards } from './components/StatsCards';
import { ActivityFeed } from './components/ActivityFeed';
import { QuickActions } from './components/QuickActions';

export default function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState<{ username: string; avatar: string } | null>(null);
  const [isActive, setIsActive] = useState(true);
  const [uptimePercentage, setUptimePercentage] = useState(100);

  const handleLogin = (userData: { username: string; avatar: string }) => {
    setUser(userData);
    setIsAuthenticated(true);
    // Clear URL parameters and redirect to home
    window.history.replaceState({}, document.title, '/');
  };

  const handleLogout = () => {
    setUser(null);
    setIsAuthenticated(false);
  };

  // Check if we're on the Discord callback route
  const isCallbackRoute = window.location.pathname === '/auth/discord/callback';

  if (isCallbackRoute) {
    return <DiscordCallback onLogin={handleLogin} />;
  }

  if (!isAuthenticated) {
    return <LoginScreen onLogin={handleLogin} />;
  }

  return (
    <div className="min-h-screen bg-neutral-50">
      <Header user={user} onLogout={handleLogout} />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
        <div className="space-y-6 sm:space-y-8">
          <StatsCards isActive={isActive} setUptimePercentage={setUptimePercentage} />
          
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 sm:gap-8 items-start">
            <div className="lg:col-span-2">
              <ActivityFeed />
            </div>
            <div className="lg:sticky lg:top-6">
              <QuickActions isActive={isActive} setIsActive={setIsActive} uptimePercentage={uptimePercentage} />
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}