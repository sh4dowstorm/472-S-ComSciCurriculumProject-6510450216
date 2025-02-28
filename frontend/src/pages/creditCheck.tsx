import React, { useState } from "react";
import Header from "../components/header";
import Button from "../components/button";
import UploadFileButton from "../components/uploadfile-button";
import "../styles/creditCheck.css";

const CreditCheckPage: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    setFile(selectedFile || null);
    setError(null);
  };

  const handleSubmit = () => {
    if (file && file.type !== "application/pdf") {
      setError("Only PDF files are allowed.");
      return;
    }
    // Logic to send data to the backend
    console.log("Data sent to backend");
  };

  return (
    <div className="credit-check-page">
      <Header />
      <div className="content">
        <div className="credit-check-container">
          <h1>Credit Check</h1>
          <div className="upload-section">
            <span className="upload-text">Upload your transcript*</span>
            <UploadFileButton onChange={handleFileChange} />
          </div>
          {error && <div className="error-popup">{error}</div>}
          <p />
          <Button text="Submit" className="button" onClick={handleSubmit} />
        </div>
      </div>
    </div>
  );
};

export default CreditCheckPage;
