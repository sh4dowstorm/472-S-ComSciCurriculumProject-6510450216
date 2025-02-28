import React, { useState } from "react";
import "../styles/uploadfile-button.css";
import { IoCloudUploadOutline, IoCloseCircleOutline } from "react-icons/io5";

interface UploadFileButtonProps {
  onChange?: (event: React.ChangeEvent<HTMLInputElement>) => void;
  buttonText?: string;
}

const UploadFileButton: React.FC<UploadFileButtonProps> = ({
  onChange,
  buttonText = "Upload File",
}) => {
  const [fileName, setFileName] = useState<string | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setFileName(file.name);
      if (onChange) {
        onChange(event);
      }
    }
  };

  const handleRemoveFile = () => {
    setFileName(null);
  };

  return (
    <div className="upload-file-button">
      <label className={"uploadfile-button"}>
        {!fileName && <IoCloudUploadOutline className="upload-icon" />}
        {fileName || buttonText}
        <input type="file" onChange={handleFileChange} />
      </label>
      {fileName && (
        <IoCloseCircleOutline
          className="delete-icon"
          onClick={handleRemoveFile}
        />
      )}
    </div>
  );
};

export default UploadFileButton;
