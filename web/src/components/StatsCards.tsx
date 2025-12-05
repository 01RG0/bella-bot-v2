import { MessageSquare, Users, Clock, Timer } from 'lucide-react';
import { useState, useEffect, useRef } from 'react';

const staticStats = [
  {
    label: 'Total Conversations',
    value: '2,847',
    change: '+12.5%',
    icon: MessageSquare,
  },
  {
    label: 'Active Users',
    value: '1,249',
    change: '+8.2%',
    icon: Users,
  },
  {
    label: 'Avg Response Time',
    value: '1.2s',
    change: '-0.3s',
    icon: Clock,
  },
];

interface StatsCardsProps {
  isActive: boolean;
  setUptimePercentage: (percentage: number) => void;
}

export function StatsCards({ isActive, setUptimePercentage }: StatsCardsProps) {
  const [uptime, setUptime] = useState(0);
  const [totalTime, setTotalTime] = useState(0);
  const accumulatedActiveTimeRef = useRef(0);
  const accumulatedTotalTimeRef = useRef(0);
  const lastStartTimeRef = useRef<number>(Date.now());

  useEffect(() => {
    // Initialize the start time when component mounts
    lastStartTimeRef.current = Date.now();
    
    const interval = setInterval(() => {
      const now = Date.now();
      const elapsed = now - lastStartTimeRef.current;
      
      // Always increment total time
      const newTotalTime = accumulatedTotalTimeRef.current + elapsed;
      setTotalTime(newTotalTime);
      
      // Only increment active time when isActive is true
      const newActiveTime = isActive 
        ? accumulatedActiveTimeRef.current + elapsed 
        : accumulatedActiveTimeRef.current;
      setUptime(newActiveTime);
      
      // Calculate uptime percentage
      if (newTotalTime > 0) {
        const percentage = (newActiveTime / newTotalTime) * 100;
        setUptimePercentage(Math.min(percentage, 100));
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [isActive, setUptimePercentage]);

  useEffect(() => {
    const now = Date.now();
    const elapsed = now - lastStartTimeRef.current;
    
    if (isActive) {
      // When resuming, just reset the start time to now
      lastStartTimeRef.current = Date.now();
    } else {
      // When pausing, save the accumulated times
      accumulatedActiveTimeRef.current = accumulatedActiveTimeRef.current + elapsed;
      accumulatedTotalTimeRef.current = accumulatedTotalTimeRef.current + elapsed;
      lastStartTimeRef.current = Date.now();
    }
  }, [isActive]);

  const formatUptime = (ms: number) => {
    const totalSeconds = Math.floor(ms / 1000);
    const hours = Math.floor(totalSeconds / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const seconds = totalSeconds % 60;
    
    return `${hours}h ${minutes}m ${seconds}s`;
  };

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
      {staticStats.map((stat) => {
        const Icon = stat.icon;
        const isPositive = stat.change.startsWith('+') || stat.change.startsWith('-0');
        
        return (
          <div
            key={stat.label}
            className="bg-white rounded-xl border border-neutral-200 p-4 sm:p-6 transition-all hover:shadow-lg hover:border-neutral-300 cursor-pointer group"
          >
            <div className="flex items-center justify-between mb-3 sm:mb-4">
              <div className="w-9 h-9 sm:w-10 sm:h-10 bg-neutral-100 rounded-lg flex items-center justify-center group-hover:bg-neutral-900 transition-colors">
                <Icon className="w-4 h-4 sm:w-5 sm:h-5 text-neutral-700 group-hover:text-white transition-colors" />
              </div>
              <span className={`text-xs px-2 py-1 rounded-full ${isPositive ? 'bg-green-50 text-green-700' : 'bg-neutral-50 text-neutral-700'}`}>
                {stat.change}
              </span>
            </div>
            <div className="space-y-1">
              <p className="text-neutral-500 text-sm">{stat.label}</p>
              <p className="text-neutral-900 text-xl sm:text-2xl">{stat.value}</p>
            </div>
          </div>
        );
      })}
      
      {/* Uptime Card */}
      <div className="bg-gradient-to-br from-neutral-900 to-neutral-800 rounded-xl border border-neutral-700 p-4 sm:p-6 transition-all hover:shadow-lg hover:border-neutral-600 cursor-pointer">
        <div className="flex items-center justify-between mb-3 sm:mb-4">
          <div className="w-9 h-9 sm:w-10 sm:h-10 bg-white/10 rounded-lg flex items-center justify-center">
            <Timer className="w-4 h-4 sm:w-5 sm:h-5 text-white" />
          </div>
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
            <span className="text-green-400 text-xs">Live</span>
          </div>
        </div>
        <div className="space-y-1">
          <p className="text-neutral-400 text-sm">Current Uptime</p>
          <p className="text-white text-lg sm:text-xl font-mono">{formatUptime(uptime)}</p>
        </div>
      </div>
    </div>
  );
}