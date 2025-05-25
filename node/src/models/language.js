import mongoose from "mongoose";

const languagePreferenceSchema = new mongoose.Schema({
  userId: {
    type: mongoose.Schema.Types.ObjectId,
    required: true,
  },
  language: {
    type: String,
    enum: ['en', 'si'], 
    default: 'en',
    required: true,
  },
  updatedAt: {
    type: Date,
    default: Date.now,
  },
});

const LanguagePreference = mongoose.model("LanguagePreference", languagePreferenceSchema);

export default LanguagePreference;
