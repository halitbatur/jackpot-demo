import './SymbolLegend.css';

const SymbolLegend = () => {
  return (
    <div className="symbol-legend">
      <h3>Symbol Guide</h3>
      <div className="legend-grid">
        <div className="legend-item">
          <span className="legend-symbol">🪙</span>
          <span className="legend-name">Vestra Coin</span>
        </div>
        <div className="legend-item">
          <span className="legend-symbol">🎭</span>
          <span className="legend-name">Brolyz</span>
        </div>
        <div className="legend-item">
          <span className="legend-symbol">👑</span>
          <span className="legend-name">CMLE head</span>
        </div>
        <div className="legend-item">
          <span className="legend-symbol">⛑️</span>
          <span className="legend-name">Vestran Helmet</span>
        </div>
        <div className="legend-item">
          <span className="legend-symbol">🎪</span>
          <span className="legend-name">Vesty</span>
        </div>
      </div>
    </div>
  );
};

export default SymbolLegend; 