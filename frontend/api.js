const API_BASE_URL = 'http://localhost:8000/api';
const USE_MOCK = true; // Cambiar a false cuando conectes tu backend real

export async function fetchTelemetryAndPrediction() {
  if (!USE_MOCK) {
    const response = await fetch(`${API_BASE_URL}/monitor`);
    if (!response.ok) throw new Error(`Error HTTP: ${response.status}`);
    return await response.json();
  }

  // Simulación del payload JSON que devolvería tu backend con el modelo ML
  const rand = (min, max) => +(Math.random() * (max - min) + min).toFixed(2);
  const v1 = rand(65, 98);
  const isAlert = v1 > 90;

  return {
    timestamp: new Date().toLocaleTimeString(),
    variables: [
      { id: 'var1', label: 'Variable 1 (Temperatura)', unit: '°C', value: v1 },
      { id: 'var2', label: 'Variable 2 (Presión)', unit: 'kPa', value: rand(100, 115) },
      { id: 'var3', label: 'Variable 3 (Frecuencia)', unit: 'Hz', value: rand(48, 62) },
      { id: 'var4', label: 'Variable 4 (Flujo)', unit: 'L/m', value: rand(12, 25) },
      { id: 'var5', label: 'Variable 5 (Voltaje)', unit: 'V', value: rand(215, 225) }
    ],
    clasificador: {
      clase: isAlert ? 'ANOMALÍA DETECTADA' : 'OPERACIÓN NORMAL',
      estado: isAlert ? 'alerta' : 'normal', // 'normal' | 'alerta' | 'critico'
      confianza: isAlert ? 94.2 : 98.7,
      probabilidades: [
        { etiqueta: 'Normal', valor: isAlert ? 5.8 : 98.7 },
        { etiqueta: 'Desviación Térmica', valor: isAlert ? 94.2 : 1.3 },
        { etiqueta: 'Fallo Crítico', valor: 0.0 }
      ],
      detalle: isAlert
        ? 'La Variable 1 supera el umbral estadístico esperado según la ventana temporal del modelo.'
        : 'Las 5 variables se mantienen dentro de los parámetros nominales de inferencia.'
    }
  };
}