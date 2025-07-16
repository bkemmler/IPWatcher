import React, { useState, useEffect, useMemo } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import axios from 'axios';
import Papa from 'papaparse';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import Settings from './Settings';

function App() {
  return (
    <Router>
      <div className="container-fluid mt-5">
        <div className="d-flex justify-content-between align-items-center mb-4">
          <h1><Link to="/">IP Watcher</Link></h1>
          <Link to="/settings" className="btn btn-secondary">Settings</Link>
        </div>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </div>
    </Router>
  );
}

function Home() {
  const [devices, setDevices] = useState([]);
  const [version, setVersion] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [sortConfig, setSortConfig] = useState({ key: 'last_seen', direction: 'descending' });

  const fetchDevices = async () => {
    try {
      const response = await axios.get('/api/devices');
      setDevices(response.data);
    } catch (error) {
      console.error("Error fetching devices:", error);
    }
  };

  const fetchVersion = async () => {
    try {
      const response = await axios.get('/api/version');
      setVersion(response.data.version);
    } catch (error) {
      console.error("Error fetching version:", error);
    }
  };

  useEffect(() => {
    fetchDevices();
    fetchVersion();
    const interval = setInterval(fetchDevices, 5000); // Refresh every 5 seconds
    return () => clearInterval(interval);
  }, []);

  const handleScan = async () => {
    try {
      await axios.post('/api/scan');
      fetchDevices();
    } catch (error) {
      console.error("Error triggering scan:", error);
    }
  };

  const handleExport = () => {
    const csv = Papa.unparse(sortedDevices);
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.setAttribute('download', 'devices.csv');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleNameChange = async (deviceId, newName) => {
    try {
      await axios.put(`/api/devices/${deviceId}`, { name: newName });
      fetchDevices();
    } catch (error) {
      console.error("Error updating device name:", error);
    }
  };

  const sortedDevices = useMemo(() => {
    let sortableDevices = [...devices];
    if (sortConfig !== null) {
      sortableDevices.sort((a, b) => {
        if (a[sortConfig.key] < b[sortConfig.key]) {
          return sortConfig.direction === 'ascending' ? -1 : 1;
        }
        if (a[sortConfig.key] > b[sortConfig.key]) {
          return sortConfig.direction === 'ascending' ? 1 : -1;
        }
        return 0;
      });
    }
    return sortableDevices;
  }, [devices, sortConfig]);

  const filteredDevices = useMemo(() => {
    return sortedDevices
      .filter(device => {
        if (statusFilter === 'all') return true;
        return statusFilter === 'online' ? device.is_online : !device.is_online;
      })
      .filter(device => {
        return Object.values(device).some(value =>
          String(value).toLowerCase().includes(searchTerm.toLowerCase())
        );
      });
  }, [sortedDevices, searchTerm, statusFilter]);

  const requestSort = (key) => {
    let direction = 'ascending';
    if (sortConfig.key === key && sortConfig.direction === 'ascending') {
      direction = 'descending';
    }
    setSortConfig({ key, direction });
  };

  const getSortDirection = (key) => {
    if (sortConfig.key === key) {
      return sortConfig.direction === 'ascending' ? '▲' : '▼';
    }
    return '';
  };

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <span className="badge bg-secondary">v{version}</span>
      </div>

      <div className="row mb-3">
        <div className="col-md-4">
          <input
            type="text"
            className="form-control"
            placeholder="Search..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        <div className="col-md-2">
          <select className="form-select" value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)}>
            <option value="all">All Statuses</option>
            <option value="online">Online</option>
            <option value="offline">Offline</option>
          </select>
        </div>
        <div className="col-md-6 d-flex justify-content-end">
          <button className="btn btn-primary me-2" onClick={handleScan}>
            Manual Scan
          </button>
          <button className="btn btn-secondary" onClick={handleExport}>
            Export CSV
          </button>
        </div>
      </div>

      <div className="table-responsive">
        <table className="table table-striped table-hover">
          <thead className="table-dark">
            <tr>
              <th onClick={() => requestSort('name')}>Name {getSortDirection('name')}</th>
              <th onClick={() => requestSort('ip_address')}>IP Address {getSortDirection('ip_address')}</th>
              <th onClick={() => requestSort('mac_address')}>MAC Address {getSortDirection('mac_address')}</th>
              <th onClick={() => requestSort('vendor')}>Vendor {getSortDirection('vendor')}</th>
              <th onClick={() => requestSort('os_details')}>OS Details {getSortDirection('os_details')}</th>
              <th onClick={() => requestSort('open_ports')}>Open Ports {getSortDirection('open_ports')}</th>
              <th onClick={() => requestSort('is_online')}>Status {getSortDirection('is_online')}</th>
              <th onClick={() => requestSort('last_seen')}>Last Seen {getSortDirection('last_seen')}</th>
            </tr>
          </thead>
          <tbody>
            {filteredDevices.map((device) => (
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
                <td>{Array.isArray(device.open_ports) ? device.open_ports.join(', ') : device.open_ports}</td>
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
    </div>
  );
}

export default App;
