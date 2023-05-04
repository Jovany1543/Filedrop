import React, { useState } from "react";
import axios from "axios";

export function DragAndDrop() {
  const [highlight, setHighlight] = useState(false);
  const [files, setFiles] = useState([]);

  function handleDragEnter(e) {
    e.preventDefault();
    setHighlight(true);
  }

  function handleDragLeave(e) {
    e.preventDefault();
    setHighlight(false);
  }

  function handleDragOver(e) {
    e.preventDefault();
  }

  function handleDrop(e) {
    e.preventDefault();
    setHighlight(false);
    const droppedFiles = Array.from(e.dataTransfer.files);
    setFiles(droppedFiles);
  }

  function handleInputChange(e) {
    const selectedFiles = Array.from(e.target.files);
    setFiles(selectedFiles);
  }

  function handleUpload() {
    const formData = new FormData();
    files.forEach((file) => {
      formData.append("files", file);
    });

    axios
      .post(process.env.BACKEND_URL + "/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      .then((response) => {
        console.log(response);
      })
      .catch((error) => {
        console.log(error);
      });
  }

  return (
    <div
      className={`drop-area ${highlight ? "highlight" : ""}`}
      onDragEnter={handleDragEnter}
      onDragLeave={handleDragLeave}
      onDragOver={handleDragOver}
      onDrop={handleDrop}
    >
      <form>
        <p>Drag and drop files here or click the button below</p>
        <input
          type="file"
          id="fileElem"
          multiple
          accept="image/*"
          onChange={handleInputChange}
        />
        <label className="button" htmlFor="fileElem">
          Upload Files
        </label>
        <button className="upload-button" onClick={handleUpload}>
          Upload
        </button>
      </form>
    </div>
  );
}
