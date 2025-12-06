export function createSocket(onMessage: (data: any) => void) {
  const apiBase = (import.meta.env.VITE_API_BASE_URL as string) ?? 'http://localhost:8000';
  // convert http(s) -> ws(s)
  const wsBase = apiBase.replace(/^http/, 'ws');
  const wsUrl = wsBase.replace(/\/+$/, '') + '/ws';

  const ws = new WebSocket(wsUrl);

  ws.onopen = () => {
    // console.log('WS connected', wsUrl);
  };

  ws.onmessage = (ev: MessageEvent) => {
    try {
      const parsed = JSON.parse(ev.data);
      onMessage(parsed);
    } catch {
      onMessage(ev.data);
    }
  };

  ws.onclose = () => {
    // console.log('WS closed');
  };

  ws.onerror = (err) => {
    console.error('WS error', err);
  };

  return ws;
}
