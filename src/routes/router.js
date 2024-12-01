import express from 'express';
import user from './user.js'
import couser from './couser.js'
import timetable from './timetable.js'
import lab  from './lab.js'
 import log from './login.js'


const router = express.Router();
import {authenticateToken,authorize} from '../utils/Authorize.js'
import word from './words.js';
// router.use('/user',authenticateToken,authorize(['ADMIN']),user)
router.use("/user", user);
router.use('/cou',couser)
router.use('/tm',timetable)
router.use('/lab',lab)
router.use('/log',log)
router.use("/word", word);

export default router

