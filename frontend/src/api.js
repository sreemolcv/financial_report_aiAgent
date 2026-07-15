import axios from "axios";

// In dev, Vite proxies /api to the FastAPI backend (see vite.config.js).
// In production, set VITE_API_BASE_URL to your deployed backend URL.

const API_BASE = import.meta.env.VITE_API_BASE_URL || "";

const client = axios.create({
    baseURL: API_BASE,
    timeout: 120000, // PDF processing / LLM calls can take a while

});

export async function getStatus(){
    const {data} = await client.get("/api/status");
    return data;
}

export async function uploadReport(file, onUploadProgress) {
    const formData = new FormData();
    formData.append("file",file);
    const { data } = await client.post("/api/upload",formData, {
        headers: {"Content-Type": "multipart/form-data"},
        onUploadProgress,
    });
    return data;
}

export async function askQuestion(question) {
    const {data} = await client.post("/api/ask", {question});
    return data;
}

export async function resetMemory() {
    const {data} = await client.post("/api/reset");
    return data;
}