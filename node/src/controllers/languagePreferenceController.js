import LanguagePreference from '../models/language.js';
import { customError } from '../utils/customeError.js';

// Create a new language preference
export const createLanguagePreference = async (req, res, next) => {
  try {
    const { userId, language } = req.body;

    // Validate input
    if (!userId || !language) {
      throw new customError('User ID and language are required', 400);
    }

    // Check if preference already exists for the user
    const existingPreference = await LanguagePreference.findOne({ userId });
    if (existingPreference) {
      throw new customError('Language preference already exists for this user', 400);
    }

    const languagePreference = new LanguagePreference({
      userId,
      language,
      updatedAt: Date.now(),
    });

    await languagePreference.save();
    res.status(201).json({
      status: 'success',
      data: languagePreference,
    });
  } catch (error) {
    next(error);
  }
};

// Update language preference
export const updateLanguagePreference = async (req, res, next) => {
  try {
    const { userId } = req.params;
    const { language } = req.body;

    // Validate input
    if (!language) {
      throw new customError('Language is required', 400);
    }

    const languagePreference = await LanguagePreference.findOneAndUpdate(
      { userId },
      { language, updatedAt: Date.now() },
      { new: true, runValidators: true }
    );

    if (!languagePreference) {
      throw new customError('Language preference not found', 404);
    }

    res.status(200).json({
      status: 'success',
      data: languagePreference,
    });
  } catch (error) {
    next(error);
  }
};

// Get language preference
export const getLanguagePreference = async (req, res, next) => {
  try {
    const { userId } = req.params;

    const languagePreference = await LanguagePreference.findOne({ userId });

    if (!languagePreference) {
      throw new customError('Language preference not found', 404);
    }

    res.status(200).json({
      status: 'success',
      data: languagePreference,
    });
  } catch (error) {
    next(error);
  }
};