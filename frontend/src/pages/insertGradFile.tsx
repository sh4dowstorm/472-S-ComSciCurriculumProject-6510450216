import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Header from "../components/header";
import Button from "../components/button";
import UploadFileButton from "../components/uploadfile-button";
import "../styles/insertGradFile.css";
import { IoWarningOutline} from "react-icons/io5";

const InsertGradFile: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [selectedPage, setSelectedPage] = useState("insertgradfile");
  const [message, setMessage] = useState<string | null>(null);
  const [messageType, setMessageType] = useState<"error" | "success" | null>(null);
  const [showConfirmPopup, setShowConfirmPopup] = useState(false);
  const [navigateTo, setNavigateTo] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    setFile(selectedFile || null);
  };

  const handleSubmit = () => {
    if (!file) {
      setMessage("ไม่สามารถตรวจสอบไฟล์ได้");
      setMessageType("error");
    } else if (file && file.type !== "application/pdf") {
      setMessage("ไฟล์แนบต้องเป็น PDF");
      setMessageType("error");
    } else {
      setMessage("ไฟล์ถูกต้อง");
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

  const handleNavigate = (page: string) => {
    if (file) {
      setShowConfirmPopup(true);
      setNavigateTo(page);
    } else {
      setSelectedPage(page);
      navigate(`/${page}`);
    }
  };

  const confirmNavigation = () => {
    if (navigateTo) {
      setSelectedPage(navigateTo);
      navigate(`/${navigateTo}`);
    }
    setShowConfirmPopup(false);
  };

  const cancelNavigation = () => {
    setShowConfirmPopup(false);
    setNavigateTo(null);
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
          <p />
          <div className="upload-container">
            <span className="upload-text"> Upload Your Transcript*</span>
            <UploadFileButton onChange={handleFileChange} />
          </div>
          <p />
          <div className="upload-container">
            <span className="upload-text">Upload Your Activity Transcript*</span>
            <UploadFileButton onChange={handleFileChange} />
          </div>
          <p />
          <div className="upload-container">
            <span className="upload-text">Upload Your Receipt*</span>
            <UploadFileButton onChange={handleFileChange} />
          </div>
          {message && (
            <div className="message-container">
              <p className={messageType === "success" ? "success-message" : "error-message"}>{message}</p>
            </div>
          )}
          <p />
          <Button text="ตรวจสอบไฟล์" className="button" onClick={handleSubmit} />
        </div>
      </div>
      {showConfirmPopup && (
        <div className="confirm-popup">
          <IoWarningOutline className="warning-icon" />
          <p>หากเปลี่ยนเป็นฟอร์ม ไฟล์ที่แนบไว้จะหายไป คุณต้องการดำเนินการต่อหรือไม่?</p>
          <Button text="ยืนยัน" className="confirm-button" onClick={confirmNavigation}/>
          <Button text="ยกเลิก" className="cancel-button" onClick={cancelNavigation}/>
        </div>
      )}
    </div>
  );
};

export default InsertGradFile;