import React, { useState, useEffect } from "react";
import Header from "../components/header";
import Button from "../components/button";
import UploadFileButton from "../components/uploadfile-button";
import "../styles/creditCheck.css";

const CreditCheckPage: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [messageType, setMessageType] = useState<"error" | "success" | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    setFile(selectedFile || null);
    
  };

  const handleSubmit = () => {
    if (file && file.type !== "application/pdf") {
      setMessage("Only PDF files are allowed.");
      setMessageType("error");
    } else {
      setMessage("Files are valid.");
      setMessageType("success");
      // Logic to send files to the backend
      console.log("Files sent to backend:", file);
    }
  };

  useEffect(() => {
      if (message) {
        const timer = setTimeout(() => {
          setMessage(null);
          setMessageType(null);
        }, 3000); // 3 seconds
  
        return () => clearTimeout(timer);
      }
    }, [message]);

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
          {message && (
            <div className="message-container">
              <p className={messageType === "success" ? "success-message" : "error-message"}>{message}</p>
            </div>
          )}
          <p />
          <Button text="Submit" className="button" onClick={handleSubmit} />
        </div>
      </div>
    </div>
  );
};

export default CreditCheckPage;
