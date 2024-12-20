import './PayoutTable.css';

const PayoutTable = () => {
  return (
    <div className="payout-table">
      <h3>Payout Table</h3>
      <div className="payout-sections">
        <div className="payout-section">
          <h4>5 of a Kind</h4>
          <div className="payout-row">
            <span>Vestra Coin x5</span>
            <span className="payout-value">10000</span>
          </div>
          <div className="payout-row">
            <span>Brolyz x5</span>
            <span className="payout-value">5000</span>
          </div>
          <div className="payout-row">
            <span>CMLE head x5</span>
            <span className="payout-value">2500</span>
          </div>
          <div className="payout-row">
            <span>Vestran Helmet x5</span>
            <span className="payout-value">1000</span>
          </div>
          <div className="payout-row">
            <span>Vesty x5</span>
            <span className="payout-value">500</span>
          </div>
        </div>

        <div className="payout-section">
          <h4>4 of a Kind</h4>
          <div className="payout-row">
            <span>Vestra Coin x4</span>
            <span className="payout-value">750</span>
          </div>
          <div className="payout-row">
            <span>Brolyz x4</span>
            <span className="payout-value">500</span>
          </div>
          <div className="payout-row">
            <span>CMLE head x4</span>
            <span className="payout-value">375</span>
          </div>
          <div className="payout-row">
            <span>Vestran Helmet x4</span>
            <span className="payout-value">250</span>
          </div>
          <div className="payout-row">
            <span>Vesty x4</span>
            <span className="payout-value">175</span>
          </div>
        </div>

        <div className="payout-section">
          <h4>3 of a Kind</h4>
          <div className="payout-row">
            <span>Vestra Coin x3</span>
            <span className="payout-value">150</span>
          </div>
          <div className="payout-row">
            <span>Brolyz x3</span>
            <span className="payout-value">125</span>
          </div>
          <div className="payout-row">
            <span>CMLE head x3</span>
            <span className="payout-value">100</span>
          </div>
          <div className="payout-row">
            <span>Vestran Helmet x3</span>
            <span className="payout-value">75</span>
          </div>
          <div className="payout-row">
            <span>Vesty x3</span>
            <span className="payout-value">50</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PayoutTable; 