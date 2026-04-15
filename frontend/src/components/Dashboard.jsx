import React from 'react';

function Dashboard({ data }) {
  const availableVehicles = data.vehicles.filter(v => v.status === 'Available').length;
  const dispatchedVehicles = data.vehicles.filter(v => v.status === 'Dispatched').length;

  return (
    <>
      <div className="glass-panel animate-fade-in" style={{ animationDelay: '0.1s' }}>
        <div className="stat-box">
          <div>
            <h3 style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>Active Cases</h3>
            <div className="stat-value">{data.active_cases}</div>
          </div>
          <div>
            <h3 style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>Available Units</h3>
            <div className="stat-value" style={{ color: '#4ade80'}}>{availableVehicles}</div>
          </div>
        </div>
      </div>

      <div className="glass-panel animate-fade-in" style={{ animationDelay: '0.2s', flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
        <h3 style={{ marginBottom: '15px' }}>Live Streamed Logs</h3>
        <div style={{ overflowY: 'auto', flexGrow: 1 }}>
          {data.recent_logs.length === 0 ? (
            <p style={{ color: 'var(--text-muted)' }}>Waiting for data stream...</p>
          ) : (
            data.recent_logs.map((log, idx) => (
              <div key={idx} className="log-item">
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span className={`badge ${log.category ? 'badge-'+log.category : 'badge-Traffic'}`}>
                    {log.category || 'Raw API'}
                  </span>
                  <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                    {log.risk_score ? `Risk: ${log.risk_score.toFixed(0)}` : 'Processing'}
                  </span>
                </div>
                <p>"{log.text || log.raw_text}"</p>
              </div>
            ))
          )}
        </div>
      </div>
    </>
  );
}

export default Dashboard;
