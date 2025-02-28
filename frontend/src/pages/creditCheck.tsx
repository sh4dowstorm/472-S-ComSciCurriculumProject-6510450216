import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import Header from "../components/header";
import "../styles/creditCheck.css";

const CreditCheckPage: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const navigate = useNavigate();

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setFile(event.target.files[0]);
    }
  };

  const handleSubmit = () => {
    if (file) {
      // Logic to send file to the backend
      console.log("File sent to backend:", file.name);
    } else {
      console.log("No file selected");
    }
  };

  return (
    <div className="credit-check-page">
      <Header />
      <div className="content">
        <div className="credit-check-container">
          <input type="file" onChange={handleFileChange} />
          <button className="button" onClick={handleSubmit}>Submit</button>
        </div>
      </div>
    </div>
  );
};

export default CreditCheckPage;
