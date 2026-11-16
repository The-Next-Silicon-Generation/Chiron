const WS_URL = 'ws://localhost:8080/ws/vitals'; // puerto del backend (T18); host fijo (T19)
const USE_MOCK = true; // Cambiar a false cuando conectes tu backend real
const STALE_MS = 5000; // sin datos nuevos en este tiempo => se descartan (igual que index.html)

// Transporte en vivo: solo WebSocket (CONV §1).
// Contrato del mensaje (T7, el mismo que index.html y app/main.py):
// { astronaut_id, name?, ts?, vitals:{ spo2, hr, rr, urine, bv }, ml?:{ triage, label, prob, flags } }
let socket = null;
let latest = null;
let latestAt = 0;

const isValid = (m) =>
  m && typeof m === 'object' && typeof m.astronaut_id === 'string' && m.astronaut_id !== '' &&
  m.vitals && typeof m.vitals === 'object';

function connect() {
  if (socket && socket.readyState <= WebSocket.OPEN) return;
  socket = new WebSocket(WS_URL);
  socket.onmessage = (e) => {
    let m;
    try { m = JSON.parse(e.data); } catch (_) { console.warn('Mensaje WebSocket no es JSON'); return; }
    if (!isValid(m)) { console.warn('Mensaje WebSocket fuera de contrato', m); return; }
    latest = m;
    latestAt = Date.now();
  };
  socket.onerror = () => { socket.close(); };
  socket.onclose = () => { socket = null; latest = null; latestAt = 0; };
}

export async function fetchTelemetryAndPrediction() {
  if (!USE_MOCK) {
    connect();
    if (!latest || Date.now() - latestAt > STALE_MS) {
      latest = null;
      throw new Error('Sin datos recientes del WebSocket');
    }
    return latest;
  }

  // Simulación de un mensaje del backend con el mismo contrato (T7)
  const rand = (min, max) => +(Math.random() * (max - min) + min).toFixed(1);
  const hr = rand(60, 125);
  const isAlert = hr > 100;

  return {
    astronaut_id: 'A-01',
    name: 'Ares',
    ts: Date.now(),
    vitals: { spo2: rand(94, 99), hr, rr: rand(12, 20), urine: rand(30, 90), bv: rand(92, 102) },
    ml: {
      triage: isAlert ? 'amber' : 'green',
      label: isAlert ? 'Pulso elevado' : 'Rangos normales',
      prob: isAlert ? 0.94 : 0.98,
      flags: { hr: isAlert ? 'amber' : 'green' }
    }
  };
}
