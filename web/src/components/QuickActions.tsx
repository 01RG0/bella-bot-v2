import { Pause, Play, RotateCcw, Download, UserPlus } from 'lucide-react';
import { useState } from 'react';

import { ImageGenerator } from './ImageGenerator';
import { BehaviorSettings } from './BehaviorSettings';

interface QuickActionsProps {
  isActive: boolean;
  setIsActive: (value: boolean) => void;
  uptimePercentage: number;
}

export function QuickActions({ isActive, setIsActive, uptimePercentage }: QuickActionsProps) {
  const [inviteUrl] = useState('https://discord.com/api/oauth2/authorize?client_id=YOUR_BOT_ID&permissions=8&scope=bot');

  const handleInviteBella = () => {
    // In production, this would open the Discord invite link
    window.open(inviteUrl, '_blank');
  };

  return (
    <div className="space-y-3 sm:space-y-4 h-full flex flex-col">
      {/* Invite Bella Card */}
      <div className="bg-gradient-to-br from-blue-600 to-blue-700 rounded-xl border border-blue-500 p-4 sm:p-5 transition-all hover:shadow-lg hover:shadow-blue-500/20">
        <div className="flex items-center justify-between mb-3 sm:mb-4">
          <div className="flex items-center gap-2 sm:gap-3">
            <div className="w-9 h-9 sm:w-10 sm:h-10 bg-white/20 rounded-lg flex items-center justify-center">
              <UserPlus className="w-4 h-4 sm:w-5 sm:h-5 text-white" />
            </div>
            <div>
              <h3 className="text-white">Invite Bella</h3>
              <p className="text-blue-100 text-xs">Add to your server</p>
            </div>
          </div>
        </div>
        <button
          onClick={handleInviteBella}
          className="w-full flex items-center justify-center gap-2 px-3 sm:px-4 py-2 sm:py-2.5 bg-white text-blue-600 rounded-lg hover:bg-blue-50 transition-all transform hover:scale-[1.02] active:scale-[0.98]"
        >
          <UserPlus className="w-4 h-4 sm:w-5 sm:h-5" />
          <span className="text-sm sm:text-base">Get Invite Link</span>
        </button>
      </div>

      <div className="bg-white rounded-xl border border-neutral-200 p-4 sm:p-5 transition-all hover:shadow-lg">
        <h2 className="text-neutral-900 mb-3 sm:mb-4">Quick Actions</h2>

        <div className="space-y-2 sm:space-y-3">
          <button
            onClick={() => setIsActive(!isActive)}
            className={`w-full flex items-center gap-2 px-3 sm:px-4 py-2 sm:py-2.5 rounded-lg transition-all transform hover:scale-[1.02] active:scale-[0.98] text-sm sm:text-base ${isActive
                ? 'bg-neutral-900 text-white hover:bg-neutral-800'
                : 'bg-green-600 text-white hover:bg-green-700'
              }`}
          >
            {isActive ? (
              <>
                <Pause className="w-4 h-4" />
                <span>Pause Bella</span>
              </>
            ) : (
              <>
                <Play className="w-4 h-4" />
                <span>Resume Bella</span>
              </>
            )}
          </button>

          <button className="w-full flex items-center gap-2 px-3 sm:px-4 py-2 sm:py-2.5 bg-white border border-neutral-200 text-neutral-900 rounded-lg hover:bg-neutral-50 hover:border-neutral-300 transition-all transform hover:scale-[1.02] active:scale-[0.98] text-sm sm:text-base">
            <RotateCcw className="w-4 h-4" />
            <span>Reset Context</span>
          </button>

          <button className="w-full flex items-center gap-2 px-3 sm:px-4 py-2 sm:py-2.5 bg-white border border-neutral-200 text-neutral-900 rounded-lg hover:bg-neutral-50 hover:border-neutral-300 transition-all transform hover:scale-[1.02] active:scale-[0.98] text-sm sm:text-base">
            <Download className="w-4 h-4" />
            <span>Export Logs</span>
          </button>

          <ImageGenerator />
          <BehaviorSettings />
        </div>
      </div>

      <div className="bg-gradient-to-br from-neutral-50 to-white rounded-xl border border-neutral-200 p-4 sm:p-5 transition-all hover:shadow-lg flex-1">
        <h3 className="text-neutral-900 mb-3 sm:mb-4">System Status</h3>
        <div className="space-y-2 sm:space-y-3">
          <div className="flex items-center justify-between p-2.5 sm:p-3 bg-white rounded-lg border border-neutral-100">
            <span className="text-neutral-600 text-xs sm:text-sm">Bot Status</span>
            <div className="flex items-center gap-2">
              <div className={`w-2 h-2 rounded-full ${isActive ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`} />
              <span className={`text-xs sm:text-sm px-2 sm:px-2.5 py-0.5 sm:py-1 rounded-full ${isActive
                  ? 'bg-green-50 text-green-700'
                  : 'bg-red-50 text-red-700'
                }`}>
                {isActive ? 'Active' : 'Paused'}
              </span>
            </div>
          </div>

          <div className="flex items-center justify-between p-2.5 sm:p-3 bg-white rounded-lg border border-neutral-100">
            <span className="text-neutral-600 text-xs sm:text-sm">Model</span>
            <span className="text-neutral-900 text-xs sm:text-sm px-2 sm:px-2.5 py-0.5 sm:py-1 bg-neutral-100 rounded-full">Gemini Flash</span>
          </div>
        </div>
      </div>
    </div>
  );
}
