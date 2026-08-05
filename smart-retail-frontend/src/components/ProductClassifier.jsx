import { useState } from "react";
import api from "../services/api";

function ProductClassifier() {
    const [file, setFile] = useState(null);
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);

    const handlePredict = async () => {
        if (!file) {
            alert("Please select an image.");
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        try {
            setLoading(true);

            const response = await api.post(
                "/classify-product",
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
            alert("Prediction failed.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="card p-4 mb-4">

            <h3>📦 Product Classification</h3>

            <input
                className="form-control mb-3"
                type="file"
                accept="image/*"
                onChange={(e) => setFile(e.target.files[0])}
            />

            <button
                className="btn btn-primary"
                onClick={handlePredict}
                disabled={loading}
            >
                {loading ? "Predicting..." : "Predict"}
            </button>

            {result && (
                <div className="alert alert-success mt-3">

                    <h5>Prediction Result</h5>

                    <p>
                        <strong>Category:</strong> {result.category}
                    </p>

                    <p>
                        <strong>Confidence:</strong> {result.confidence}%
                    </p>

                </div>
            )}

        </div>
    );
}

export default ProductClassifier;