import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Header from "../components/header";
import "../styles/InsertGradFile.css";

const InsertGradFile: React.FC = () => {
  const [files, setFiles] = useState<{ [key: string]: File | null }>({
    transcript: null,
    activityTranscript: null,
    receipt: null,
  });
  const [selectedPage, setSelectedPage] = useState("insertgradfile");
  const [message, setMessage] = useState<string | null>(null);
  const [messageType, setMessageType] = useState<"error" | "success" | null>(null);
  const navigate = useNavigate();

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>, fileType: string) => {
    if (event.target.files) {
      const selectedFile = event.target.files[0];
      setFiles((prevFiles) => ({ ...prevFiles, [fileType]: selectedFile }));
    }
  };

  const handleSubmit = () => {
    const invalidFiles = Object.values(files).filter(
      (file) => file && file.type !== "application/pdf"
    );

    if (invalidFiles.length > 0) {
      setMessage("Only PDF files are allowed.");
      setMessageType("error");
    } else {
      setMessage("Files are valid.");
      setMessageType("success");
      // Logic to send files to the backend
      console.log("Files sent to backend:", files);
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

  const handleNavigate = (page: string) => {
    setSelectedPage(page);
    navigate(`/${page}`);
  };

  return (
    <div className="grad-file-page">
      <Header />
      <div className="content">
        <div className="grad-file-container">
          <div className="button-container">
            <label>
              <input
                type="radio"
                name="page"
                value="insertgradfile"
                checked={selectedPage === "insertgradfile"}
                onChange={() => handleNavigate("insertgradfile")}
              />
              Insert Graduation File
            </label>
            <label>
              <input
                type="radio"
                name="page"
                value="creditcheck"
                checked={selectedPage === "creditcheck"}
                onChange={() => handleNavigate("creditcheck")}
              />
              Credit Check
            </label>
          </div>
          <div className="upload-container">
            <span>Upload Your Transcript*</span>
            <input type="file" onChange={(e) => handleFileChange(e, "transcript")} />
          </div>
          <div className="upload-container">
            <span>Upload Your Activity Transcript*</span>
            <input type="file" onChange={(e) => handleFileChange(e, "activityTranscript")} />
          </div>
          <div className="upload-container">
            <span>Upload Your Receipt*</span>
            <input type="file" onChange={(e) => handleFileChange(e, "receipt")} />
          </div>
          {message && (
            <div className="message-container">
              <p className={messageType === "success" ? "success-message" : "error-message"}>{message}</p>
            </div>
          )}
          <button className="button" onClick={handleSubmit}>Inspect Files</button>
        </div>
      </div>
    </div>
  );
};

export default InsertGradFile;