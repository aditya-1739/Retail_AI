import { useState } from "react";
import api from "../services/api";

function Chatbot() {
    const [message, setMessage] = useState("");
    const [chat, setChat] = useState([]);
    const [loading, setLoading] = useState(false);

    const sendMessage = async () => {
        if (!message.trim()) return;

        const userMessage = message;

        // Show user message immediately
        setChat((prev) => [...prev, { sender: "You", text: userMessage }]);
        setMessage("");

        try {
            setLoading(true);

            const response = await api.post("/chat", {
                message: userMessage,
            });

            setChat((prev) => [
                ...prev,
                {
                    sender: "Bot",
                    text: response.data.response,
                },
            ]);
        } catch (error) {
            console.error(error);

            setChat((prev) => [
                ...prev,
                {
                    sender: "Bot",
                    text: "Sorry, something went wrong.",
                },
            ]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="card p-4 mb-4">

            <h3>💬 SmartRetailAI Chatbot</h3>

            <div
                className="border rounded p-3 mb-3"
                style={{
                    height: "300px",
                    overflowY: "auto",
                    backgroundColor: "#f8f9fa",
                }}
            >
                {chat.length === 0 ? (
                    <p className="text-muted">
                        Start chatting...
                    </p>
                ) : (
                    chat.map((msg, index) => (
                        <div key={index} className="mb-2">
                            <strong>{msg.sender}:</strong> {msg.text}
                        </div>
                    ))
                )}
            </div>

            <div className="input-group">

                <input
                    type="text"
                    className="form-control"
                    placeholder="Type your message..."
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    onKeyDown={(e) => {
                        if (e.key === "Enter") {
                            sendMessage();
                        }
                    }}
                />

                <button
                    className="btn btn-primary"
                    onClick={sendMessage}
                    disabled={loading}
                >
                    {loading ? "Sending..." : "Send"}
                </button>

            </div>

        </div>
    );
}

export default Chatbot;