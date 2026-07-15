import { useRef, useState } from "react";
import { Plus, FileText } from "lucide-react";
import { uploadReport } from "../api";

export default function FileUpload({ onUploaded, disabled }) {
  const fileInputRef = useRef(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState(null);

  function handlePillClick() {
    fileInputRef.current?.click();
  }

  async function handleFileChange(e) {
    const file = e.target.files?.[0];
    if (!file) return;
    setSelectedFile(file);
    setError(null);
    await handleProcess(file);
  }

  async function handleProcess(file) {
    setUploading(true);
    setError(null);
    setProgress(0);
    try {
      const result = await uploadReport(file, (evt) => {
        if (evt.total) {
          setProgress(Math.round((evt.loaded * 100) / evt.total));
        }
      });
      onUploaded(result);
    } catch (err) {
      const detail =
        err?.response?.data?.detail || err.message || "Upload failed.";
      setError(detail);
    } finally {
      setUploading(false);
    }
  }

  return (
    <div className="upload-card">
      <input
        ref={fileInputRef}
        type="file"
        accept="application/pdf"
        onChange={handleFileChange}
        disabled={disabled || uploading}
        style={{ display: "none" }}
      />

      <button
        className="new-chat-pill"
        onClick={handlePillClick}
        disabled={disabled || uploading}
      >
        <Plus size={16} strokeWidth={2.25} />
        <span>{uploading ? `Processing... ${progress}%` : "New report"}</span>
      </button>

      {selectedFile && !uploading && !error && (
        <p className="selected-file">
          <FileText size={13} />
          {selectedFile.name}
        </p>
      )}

      {error && <p className="error-text">{error}</p>}
    </div>
  );
}