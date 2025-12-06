import { useState, useEffect } from "react";
import { RefreshCcw } from "lucide-react";
import { Button } from "./ui/button";
import { API_BASE_URL } from '../config';

interface LogEntry {
    _id: string;
    timestamp: number;
    type: string;
    message: string;
    level: string;
    details: any;
}

export function LogsPanel() {
    const [logs, setLogs] = useState<LogEntry[]>([]);
    const [loading, setLoading] = useState(false);

    const fetchLogs = async () => {
        setLoading(true);
        try {
            const res = await fetch(`${API_BASE_URL}/api/logs?limit=50`);
            const data = await res.json();
            if (data.logs) {
                setLogs(data.logs);
            }
        } catch (e) {
            console.error(e);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchLogs();
        const interval = setInterval(fetchLogs, 10000);
        return () => clearInterval(interval);
    }, []);

    const getLevelColor = (level: string) => {
        switch (level) {
            case "ERROR": return "bg-red-500";
            case "WARN": return "bg-yellow-500";
            default: return "bg-blue-500";
        }
    };

    return (
        <div className="bg-white rounded-xl border border-neutral-200 p-4 sm:p-5 h-[600px] flex flex-col">
            <div className="flex justify-between items-center mb-4">
                <h2 className="text-lg font-semibold text-neutral-900">System Logs</h2>
                <Button variant="outline" size="sm" onClick={fetchLogs} disabled={loading}>
                    <RefreshCcw className={`w-4 h-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
                    Refresh
                </Button>
            </div>

            <div className="flex-1 overflow-y-auto space-y-2 pr-2">
                {logs.length === 0 ? (
                    <div className="text-center text-neutral-400 py-10">No logs found</div>
                ) : (
                    logs.map((log) => (
                        <div key={log._id} className="p-3 bg-neutral-50 rounded-lg border border-neutral-100 text-sm hover:border-blue-200 transition-colors">
                            <div className="flex justify-between items-start mb-1">
                                <div className="flex items-center gap-2">
                                    <span className={`px-2 py-0.5 rounded text-[10px] font-bold text-white ${getLevelColor(log.level)}`}>
                                        {log.level}
                                    </span>
                                    <span className="font-mono text-xs text-neutral-500">
                                        {new Date(log.timestamp * 1000).toLocaleString()}
                                    </span>
                                </div>
                                <span className="text-xs font-medium text-neutral-400 uppercase tracking-wider">
                                    {log.type}
                                </span>
                            </div>
                            <p className="text-neutral-800 font-medium break-words">{log.message}</p>
                            {log.details && Object.keys(log.details).length > 0 && (
                                <div className="mt-2 text-xs bg-white border border-neutral-200 p-2 rounded overflow-x-auto font-mono text-neutral-600">
                                    {JSON.stringify(log.details, null, 2)}
                                </div>
                            )}
                        </div>
                    ))
                )}
            </div>
        </div>
    );
}
