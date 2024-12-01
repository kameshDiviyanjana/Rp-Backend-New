import mongoose from "mongoose";
import { autoInc } from "auto-increment-group";

const wordmodle = new mongoose.Schema({
  sl: {
    type: String,
  },
  wordAdd: {
    type: String,
    required: true,
  },
  userid: {
    type: String,
    required: true,
  },
  imagewordUrl: {
    type: String,
  },
});
wordmodle.plugin(autoInc, {
  field: "sl",
  digits: 4,
  startAt: 1,
  incrementBy: 1,
  unique: false,
});
const words = mongoose.model("Word", wordmodle);

export default words;
