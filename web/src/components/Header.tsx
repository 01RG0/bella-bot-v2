import { Bot, Settings, LogOut } from 'lucide-react';

interface HeaderProps {
  user: { username: string; avatar: string } | null;
  onLogout: () => void;
}

export function Header({ user, onLogout }: HeaderProps) {
  return (
    <header className="bg-white border-b border-neutral-200 sticky top-0 z-50 backdrop-blur-sm bg-white/80">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-14 sm:h-16">
          <div className="flex items-center gap-2 sm:gap-3">
            <div className="w-8 h-8 sm:w-10 sm:h-10 bg-gradient-to-br from-neutral-900 to-neutral-700 rounded-lg flex items-center justify-center shadow-md">
              <Bot className="w-5 h-5 sm:w-6 sm:h-6 text-white" />
            </div>
            <div>
              <h1 className="text-neutral-900 text-base sm:text-lg">Bella</h1>
              <p className="text-xs text-neutral-500 hidden sm:block">AI Assistant Dashboard</p>
            </div>
          </div>
          
          <div className="flex items-center gap-1 sm:gap-2">
            {user && (
              <div className="flex items-center gap-2 sm:gap-3 px-2 sm:px-3 py-1.5 sm:py-2 rounded-lg hover:bg-neutral-50 transition-colors cursor-pointer">
                <img 
                  src={user.avatar} 
                  alt={user.username}
                  className="w-7 h-7 sm:w-8 sm:h-8 rounded-full ring-2 ring-neutral-200"
                />
                <span className="text-neutral-700 text-sm hidden sm:block">{user.username}</span>
              </div>
            )}
            <button className="w-9 h-9 sm:w-10 sm:h-10 flex items-center justify-center rounded-lg hover:bg-neutral-100 transition-all active:scale-95">
              <Settings className="w-4 h-4 sm:w-5 sm:h-5 text-neutral-600" />
            </button>
            <button 
              onClick={onLogout}
              className="w-9 h-9 sm:w-10 sm:h-10 flex items-center justify-center rounded-lg hover:bg-red-50 transition-all active:scale-95 group"
            >
              <LogOut className="w-4 h-4 sm:w-5 sm:h-5 text-neutral-600 group-hover:text-red-600 transition-colors" />
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}