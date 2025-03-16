import mongoose from "mongoose";
import { autoInc } from "auto-increment-group";

const scoremodle = new mongoose.Schema({
  sl: {
    type: String,
  },
  marks: {
    type: Number,
    default: 0,
    //required: true,
  },
  userid: {
    type: String,
    required: true,
  },
});
scoremodle.plugin(autoInc, {
  field: "sl",
  digits: 4,
  startAt: 1,
  incrementBy: 1,
  unique: false,
});
const score = mongoose.model("Score", scoremodle);

export default score;
