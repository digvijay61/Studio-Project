import React, { useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline, useMap } from 'react-leaflet';
import L from 'leaflet';

// Fix Leaflet's default icon path issues in React
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

// Custom icons based on vehicle status
const getMarkerIcon = (status) => {
  const color = status === 'Available' ? 'green' : status === 'Dispatched' ? 'red' : 'gray';
  
  return new L.DivIcon({
    className: 'custom-icon',
    html: `<div style="background-color: ${color}; width: 14px; height: 14px; border-radius: 50%; border: 2px solid white; box-shadow: 0 0 5px rgba(0,0,0,0.5);"></div>`,
    iconSize: [14, 14],
    iconAnchor: [7, 7]
  });
};

function MapComponent({ vehicles, logs }) {
  const center = [40.7580, -73.9855]; // Centered on NY mock data

  // Extract routes from logs if they were generated
  const activeRoutes = logs
    .filter(log => log.route && log.status === 'Dispatched')
    .map(log => log.route);

  return (
    <MapContainer center={center} zoom={12} style={{ height: '100%', width: '100%' }}>
      {/* Dark theme map tiles */}
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
        url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
      />
      
      {vehicles.map((v) => (
        <Marker key={v.id} position={[v.lat, v.lng]} icon={getMarkerIcon(v.status)}>
          <Popup>
            <div>
              <strong>{v.vehicle_type}</strong><br/>
              Status: {v.status}
            </div>
          </Popup>
        </Marker>
      ))}

      {logs.map((log) => {
        if (!log.lat || !log.lng) return null;
        return (
          <Marker key={log._id} position={[log.lat, log.lng]}>
             <Popup>
                <div>
                  <strong>{log.category || 'Incident'}</strong><br/>
                  {log.text || log.raw_text}
                </div>
             </Popup>
          </Marker>
        );
      })}

      {activeRoutes.map((routeCoords, idx) => (
        <Polyline key={idx} positions={routeCoords} color="#3b82f6" weight={4} dashArray="10, 10" />
      ))}
    </MapContainer>
  );
}

export default MapComponent;
