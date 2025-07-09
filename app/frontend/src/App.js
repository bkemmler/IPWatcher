import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Papa from 'papaparse';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  const [devices, setDevices] = useState([]);
  const [version, setVersion] = useState('');

  const fetchDevices = async () => {
    const response = await axios.get('/api/devices');
    setDevices(response.data);
  };

  const fetchVersion = async () => {
    const response = await axios.get('/api/version');
    setVersion(response.data.version);
  };

  useEffect(() => {
    fetchDevices();
    fetchVersion();
  }, []);

  const handleScan = async () => {
    await axios.post('/api/scan');
    fetchDevices();
  };

  const handleExport = () => {
    const csv = Papa.unparse(devices);
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.setAttribute('download', 'devices.csv');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleNameChange = async (deviceId, newName) => {
    await axios.put(`/api/devices/${deviceId}`, { name: newName });
    fetchDevices();
  };

  return (
    <div className="container mt-5">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h1>IP Watcher</h1>
        <span className="badge bg-secondary">v{version}</span>
      </div>

      <div className="d-flex justify-content-end mb-3">
        <button className="btn btn-primary me-2" onClick={handleScan}>
          Manual Scan
        </button>
        <button className="btn btn-secondary" onClick={handleExport}>
          Export CSV
        </button>
      </div>

      <table className="table table-striped">
        <thead>
          <tr>
            <th>Name</th>
            <th>IP Address</th>
            <th>MAC Address</th>
            <th>Vendor</th>
            <th>OS Details</th>
            <th>Open Ports</th>
            <th>Status</th>
            <th>Last Seen</th>
          </tr>
        </thead>
        <tbody>
          {devices.map((device) => (
            <tr key={device.id}>
              <td>
                <input
                  type="text"
                  className="form-control"
                  defaultValue={device.name}
                  onBlur={(e) => handleNameChange(device.id, e.target.value)}
                />
              </td>
              <td>{device.ip_address}</td>
              <td>{device.mac_address}</td>
              <td>{device.vendor}</td>
              <td>{device.os_details}</td>
              <td>{device.open_ports}</td>
              <td>
                <span className={`badge ${device.is_online ? 'bg-success' : 'bg-danger'}`}>
                  {device.is_online ? 'Online' : 'Offline'}
                </span>
              </td>
              <td>{new Date(device.last_seen).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;