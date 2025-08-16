import React from "react";
import Camera from "../component/Camera";
import FetchData from "../component/FetchData";

const App = () => (
  <div style={{ minHeight: '100vh', backgroundColor: '#f7fafc', fontFamily: 'sans-serif' }}>
    {/* Navigation Bar */}
    <nav style={{ backgroundColor: '#ffffff', boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)' }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '16px 24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1 style={{ fontSize: '24px', fontWeight: 'bold', color: '#3b82f6' }}>Safety Monitor</h1>
        <ul style={{ display: 'flex', gap: '24px' }}>
          <li style={{ color: '#4b5563', cursor: 'pointer', transition: 'color 0.3s' }} onMouseEnter={e => e.currentTarget.style.color = '#3b82f6'} onMouseLeave={e => e.currentTarget.style.color = '#4b5563'}>Home</li>
          <li style={{ color: '#4b5563', cursor: 'pointer', transition: 'color 0.3s' }} onMouseEnter={e => e.currentTarget.style.color = '#3b82f6'} onMouseLeave={e => e.currentTarget.style.color = '#4b5563'}>About</li>
        </ul>
      </div>
    </nav>

    {/* Main Content */}
    <main style={{ maxWidth: '1200px', margin: '0 auto', padding: '24px', display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* Camera Section */}
      <section style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        <h2 style={{ fontSize: '20px', fontWeight: '600', color: '#1f2937', marginBottom: '16px', textAlign: 'center' }}>
          Real-Time Violence Detection
        </h2>
        <Camera />
      </section>

      {/* FetchData Section */}
      <section style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        <h2 style={{ fontSize: '20px', fontWeight: '600', color: '#1f2937', marginBottom: '16px', textAlign: 'center' }}>
          Threat Log
        </h2>
        <div style={{ flex: 1, minHeight: '256px', backgroundColor: '#ffffff', borderRadius: '8px', boxShadow: 'inset 0 1px 3px rgba(0, 0, 0, 0.1)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#9ca3af' }}>
          <FetchData />
        </div>
      </section>
    </main>
  </div>
);

export default App;
