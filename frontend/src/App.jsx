import React, { useState, useEffect } from 'react';
import axios from 'axios';
import MapComponent from './components/Map';
import Dashboard from './components/Dashboard';
import EmergencyInput from './components/EmergencyInput';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function App() {
  const [dashboardData, setDashboardData] = useState({
    active_cases: 0,
    vehicles: [],
    recent_logs: []
  });

  const fetchData = async () => {
    try {
      const res = await axios.get(`${API_URL}/dashboard-data`);
      setDashboardData(res.data);
    } catch (err) {
      console.error("Failed to fetch dashboard data");
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  const handleNewEmergency = async (text, lat, lng) => {
    try {
      // 1. Classify
      const clsRes = await axios.post(`${API_URL}/classify-emergency`, { text, lat, lng });
      const { category, risk_score } = clsRes.data;

      // 2. Dispatch
      // Use fake case ID for immediate flow, real one is created in backend but we can just use a timestamp for dispatch payload
      const tempId = `TEMP-${Date.now()}`;
      await axios.post(`${API_URL}/dispatch?case_id=${tempId}&lat=${lat}&lng=${lng}&category=${category}`);

      // Refresh Dashboard instantly
      fetchData();
      alert(`Emergency Classified as ${category} (Risk: ${risk_score.toFixed(1)}). Unit Dispatched!`);

    } catch (err) {
      console.error(err);
      alert("Error processing emergency. Ensure vehicles are available.");
    }
  };

  return (
    <div className="app-container">
      <header className="app-header glass-panel">
        <h1>ResponderAI</h1>
        <div>Live City Overview</div>
      </header>

      <aside className="app-sidebar">
        <EmergencyInput onSubmit={handleNewEmergency} />
        <Dashboard data={dashboardData} />
      </aside>

      <main className="app-main">
        <MapComponent vehicles={dashboardData.vehicles} logs={dashboardData.recent_logs} />
      </main>
    </div>
  );
}

export default App;
