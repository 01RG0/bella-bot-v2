import { TrendingUp, TrendingDown, Activity } from 'lucide-react';
import { useEffect, useState } from 'react';
import { createSocket } from '../utils/socket';

const metrics = [
  {
    id: 1,
    category: 'Conversations',
    current: 847,
    previous: 756,
    timeframe: 'Last 24 hours',
  },
  {
    id: 2,
    category: 'New Users',
    current: 124,
    previous: 98,
    timeframe: 'Last 24 hours',
  },
  {
    id: 3,
    category: 'Messages Sent',
    current: 3421,
    previous: 3789,
    timeframe: 'Last 24 hours',
  },
  {
    id: 4,
    category: 'Avg. Session Time',
    current: 8.4,
    previous: 7.9,
    timeframe: 'Last 24 hours',
    unit: 'min',
  },
  {
    id: 5,
    category: 'Response Rate',
    current: 97.2,
    previous: 96.8,
    timeframe: 'Last 24 hours',
    unit: '%',
  },
  {
    id: 6,
    category: 'Error Rate',
    current: 0.8,
    previous: 1.2,
    timeframe: 'Last 24 hours',
    unit: '%',
  },
];

export function ActivityFeed() {
  const [events, setEvents] = useState<Array<string>>([]);

  useEffect(() => {
    const ws = createSocket((data) => {
      // normalize to a short string for display
      let text = '';
      try {
        if (typeof data === 'string') text = data;
        else if (data.type) text = `${data.type}: ${JSON.stringify(data.payload ?? data)}`;
        else text = JSON.stringify(data);
      } catch {
        text = String(data);
      }

      setEvents((prev) => [text, ...prev].slice(0, 10));
    });

    return () => ws.close();
  }, []);

  return (
    <div className="bg-white rounded-xl border border-neutral-200 p-4 sm:p-6 transition-all hover:shadow-lg h-full flex flex-col">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between mb-4 sm:mb-6 gap-3 sm:gap-0">
        <h2 className="text-neutral-900">Performance Metrics</h2>
        <div className="flex items-center gap-2 text-green-600 text-sm bg-green-50 px-3 py-1.5 rounded-full w-fit">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
          <Activity className="w-4 h-4" />
          <span>Live</span>
        </div>
      </div>

      {events.length > 0 && (
        <div className="mb-4">
          <h3 className="text-sm text-neutral-600 mb-2">Live Events</h3>
          <div className="space-y-2 max-h-36 overflow-auto">
            {events.map((e, i) => (
              <div key={i} className="text-xs text-neutral-700 bg-neutral-50 border border-neutral-100 rounded px-3 py-2">{e}</div>
            ))}
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4 flex-1">
        {metrics.map((metric) => {
          const change = metric.current - metric.previous;
          const percentChange = ((change / metric.previous) * 100).toFixed(1);
          const isPositive = change > 0;
          const isNegative = change < 0;
          
          // For error rate, inverse the positive/negative meaning
          const showPositive = metric.category === 'Error Rate' ? isNegative : isPositive;
          const showNegative = metric.category === 'Error Rate' ? isPositive : isNegative;
          
          return (
            <div
              key={metric.id}
              className="border border-neutral-200 rounded-lg p-3 sm:p-4 transition-all hover:border-neutral-300 hover:shadow-md cursor-pointer group"
            >
              <div className="flex items-start justify-between mb-2 sm:mb-3">
                <div className="flex-1">
                  <p className="text-neutral-600 text-sm group-hover:text-neutral-900 transition-colors">{metric.category}</p>
                  <p className="text-neutral-900 text-xl sm:text-2xl mt-1">
                    {metric.current.toLocaleString()}
                    {metric.unit && <span className="text-base sm:text-lg ml-1">{metric.unit}</span>}
                  </p>
                </div>
                
                <div className={`flex items-center gap-1 px-2 sm:px-2.5 py-1 sm:py-1.5 rounded-lg transition-all ${
                  showPositive ? 'bg-green-50 text-green-700 group-hover:bg-green-100' : 
                  showNegative ? 'bg-red-50 text-red-700 group-hover:bg-red-100' : 
                  'bg-neutral-50 text-neutral-700 group-hover:bg-neutral-100'
                }`}>
                  {showPositive && <TrendingUp className="w-3 sm:w-4 h-3 sm:h-4" />}
                  {showNegative && <TrendingDown className="w-3 sm:w-4 h-3 sm:h-4" />}
                  <span className="text-xs">
                    {isPositive ? '+' : ''}{percentChange}%
                  </span>
                </div>
              </div>
              
              <div className="flex items-center justify-between">
                <p className="text-neutral-400 text-xs">{metric.timeframe}</p>
                <p className="text-neutral-400 text-xs">
                  prev: {metric.previous.toLocaleString()}{metric.unit || ''}
                </p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}