import {addtimetable,findsubjje,findbydatecontroller} from '../controllers/timetable.js'
import {authenticateToken,authorize} from '../utils/Authorize.js'
import express from 'express';

const timetable = express.Router();

timetable.post('/',authenticateToken,authorize(['ADMIN']),addtimetable)
timetable.get('/:subjectName',authenticateToken,authorize(['ADMIN','Student', 'lecture']),findsubjje)
timetable.get('/mk/:tadate',authenticateToken,authorize(['ADMIN','Student', 'lecture']),findbydatecontroller)



export default timetable