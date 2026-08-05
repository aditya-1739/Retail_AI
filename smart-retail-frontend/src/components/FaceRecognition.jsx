import { useState } from "react";
import api from "../services/api";

function FaceRecognition() {
    const [file, setFile] = useState(null);
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleRecognize = async () => {
        if (!file) {
            alert("Please select a face image.");
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        try {
            setLoading(true);

            const response = await api.post(
                "/recognize-face",
                formData,
                {
                    headers: {
                        "Content-Type": "multipart/form-data",
                    },
                }
            );

            setResult(response.data);

        } catch (error) {
            console.error(error);
            alert("Face recognition failed.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="card p-4 mb-4">

            <h3>😊 Face Recognition</h3>

            <input
                type="file"
                className="form-control mb-3"
                accept="image/*"
                onChange={(e) => setFile(e.target.files[0])}
            />

            <button
                className="btn btn-success"
                onClick={handleRecognize}
                disabled={loading}
            >
                {loading ? "Recognizing..." : "Recognize Face"}
            </button>

            {result && (
                <div className="alert alert-info mt-3">

                    <h5>Recognition Result</h5>

                    <p>
                        <strong>Person ID:</strong> {result.person_id}
                    </p>

                    <p>
                        <strong>Confidence:</strong> {result.confidence}%
                    </p>

                </div>
            )}

        </div>
    );
}

export default FaceRecognition;