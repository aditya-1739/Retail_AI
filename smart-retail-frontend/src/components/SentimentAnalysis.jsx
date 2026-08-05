import { useState } from "react";
import api from "../services/api";

function SentimentAnalysis() {
    const [review, setReview] = useState("");
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleAnalyze = async () => {
        if (!review.trim()) {
            alert("Please enter a review.");
            return;
        }

        try {
            setLoading(true);

            const response = await api.post("/analyze-review", {
                review: review,
            });

            setResult(response.data);
        } catch (error) {
            console.error(error);
            alert("Sentiment analysis failed.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="card p-4 mb-4">

            <h3>⭐ Sentiment Analysis</h3>

            <textarea
                className="form-control mb-3"
                rows="4"
                placeholder="Enter a product review..."
                value={review}
                onChange={(e) => setReview(e.target.value)}
            />

            <button
                className="btn btn-warning"
                onClick={handleAnalyze}
                disabled={loading}
            >
                {loading ? "Analyzing..." : "Analyze Review"}
            </button>

            {result && (
                <div className="alert alert-success mt-3">

                    <h5>Analysis Result</h5>

                    <p>
                        <strong>Review:</strong> {result.review}
                    </p>

                    <p>
                        <strong>Sentiment:</strong> {result.sentiment}
                    </p>

                </div>
            )}

        </div>
    );
}

export default SentimentAnalysis;