import React from "react";
import Header from "../components/header";
import Button from "../components/button";
import "../styles/creditCheck.css";

const CreditCheckPage: React.FC = () => {
  const handleSubmit = () => {
    // Logic to send data to the backend
    console.log("Data sent to backend");
  };

  return (
    <div className="credit-check-page">
      <Header />
      <div className="content">
        <div className="credit-check-container">
          <h1>Credit Check</h1>
          <Button
            text="Submit"
            className="button"
            onClick={handleSubmit}
          />
        </div>
      </div>
    </div>
  );
};

export default CreditCheckPage;
