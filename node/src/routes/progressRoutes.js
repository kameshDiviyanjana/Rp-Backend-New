import express from 'express';
import { saveProgress, getUserProgress } from '../controllers/progressController.js';

const router = express.Router();

router.post('/addProgress', saveProgress);
router.get('/progress/:userId', getUserProgress);

export const progressRoutes = router;
