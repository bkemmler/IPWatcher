import React, { useState, useEffect } from 'react';

function Settings() {
  const [config, setConfig] = useState(null);

  useEffect(() => {
    fetch('/api/config')
      .then(response => response.json())
      .then(data => setConfig(data));
  }, []);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setConfig(prevConfig => ({
      ...prevConfig,
      [name]: value
    }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    fetch('/api/config', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(config),
    })
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data);
      alert('Settings saved successfully!');
    })
    .catch((error) => {
      console.error('Error:', error);
      alert('Error saving settings.');
    });
  };

  if (!config) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h2>Settings</h2>
      <form onSubmit={handleSubmit}>
        <label>
          IP Ranges:
          <input type="text" name="ip_ranges" value={config.ip_ranges.join(', ')} onChange={e => setConfig({...config, ip_ranges: e.target.value.split(', ')})} />
        </label>
        <br />
        <label>
          Deep Scan Schedule:
          <input type="text" name="deep_scan_schedule" value={config.deep_scan_schedule} onChange={handleChange} />
        </label>
        <br />
        <label>
          Ping Sweep Interval:
          <input type="number" name="ping_sweep_interval" value={config.ping_sweep_interval} onChange={handleChange} />
        </label>
        <br />
        <button type="submit">Save</button>
      </form>
    </div>
  );
}

export default Settings;
