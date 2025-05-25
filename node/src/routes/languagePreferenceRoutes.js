import express from 'express';
import { 
  createLanguagePreference, 
  updateLanguagePreference, 
  getLanguagePreference 
} from '../controllers/languagePreferenceController.js';

const router = express.Router();

// Routes for language preferences
router.post('/', createLanguagePreference);
router.put('/update/:userId', updateLanguagePreference);
router.get('/get/:userId', getLanguagePreference);

export default router;