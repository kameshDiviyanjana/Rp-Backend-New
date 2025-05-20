import Progress from '../models/progress.js';
import mongoose from 'mongoose';

// Create or  progress
export const saveProgress = async (req, res) => {
  const { userId, skillType, subSkill, score } = req.body;

  try {
    // Create a new Progress record without checking for existing records
    const progress = new Progress({ userId, skillType, subSkill, score });
    await progress.save();

    res.status(201).json({ message: "Progress saved", data: progress });
  } catch (error) {
    console.error("Error saving progress:", error);
    res.status(500).json({ error: "Failed to save progress" });
  }
};

// Get all progress for a user
export const getUserProgress = async (req, res) => {

  const { userId } = req.params;

  // Validate userId
  if (!userId) {
    return res.status(400).json({ error: "User ID is required" });
  }

  // Check if userId is a valid ObjectId
  if (!mongoose.Types.ObjectId.isValid(userId)) {
    return res.status(400).json({ error: "Invalid user ID format" });
  }

  try {

    const progress = await Progress.find({ userId: new mongoose.Types.ObjectId(userId) });

   
    res.status(200).json({ data: progress });
  } catch (error) {
    console.error("🔥 Error fetching progress from MongoDB:", {
      message: error.message,
      stack: error.stack,
    });
    res.status(500).json({ error: "Failed to fetch progress" });
  }
};
