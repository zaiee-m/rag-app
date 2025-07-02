import { useState } from "react";

const UploadStatus = {
    IDLE: 'idle',
    UPLOADING: 'uploading',
    SUCCESS: 'success',
    ERROR: 'error'
};

export default function FileUploader() {

    const [file, setFile] = useState(null);
    const [status, setStatus] = useState(null);

    async function handleFileChange(event) {
        if (event.target.files) {
            const selectedFile = event.target.files[0];
            setFile(selectedFile);
            await uploadFile(selectedFile); // Call the upload function
        }
    }

    async function uploadFile(file) {
        setStatus(UploadStatus.UPLOADING);
        const formData = new FormData();
        formData.append('file', file);

        let response = null;
        try {
            response = await fetch("http://127.0.0.1:5000/docs/upload", {
                method: "POST",
                body: formData
            });

            if (response.ok) {
                const result = await response.json();
                console.log(result);
                setStatus(UploadStatus.SUCCESS);
            } else {
                const errorResponse = await response.json(); 
                console.error("Upload failed:", response.status, errorResponse);
                setStatus(UploadStatus.ERROR);
            }

        } catch (error) {
            console.error("Error during upload:", JSON.stringify(error));
            setStatus(UploadStatus.ERROR);
        }
    }

    return (
        <div>
            <input type="file" onChange={handleFileChange}/>
        </div>
    );
}