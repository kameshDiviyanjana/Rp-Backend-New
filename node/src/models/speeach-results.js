import mongoose from "mongoose";

const SpeechResultsmodul = new mongoose.Schema({
  cluster: {
    type: String,
    required: [true, "cluster number is required"],
  },
  confidence: {
    type: String,
    required: [true, "confidence is required"],
  },
  date: {
    type: Date, // Changed to Date type for proper querying
  },
  userid: {
    type: String,
  },
});

const speech = mongoose.model("resultspeech", SpeechResultsmodul);

export default speech;
