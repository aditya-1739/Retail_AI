import ProductClassifier from "../components/ProductClassifier";
import FaceRecognition from "../components/FaceRecognition";
import SentimentAnalysis from "../components/SentimentAnalysis";
import Chatbot from "../components/Chatbot";

function Home() {
    return (
        <div className="container mt-4">
            <ProductClassifier />
            <FaceRecognition />
            <SentimentAnalysis />
            <Chatbot />
        </div>
    );
}

export default Home;