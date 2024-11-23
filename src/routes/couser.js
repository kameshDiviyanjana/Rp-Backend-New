import express from 'express';
import {removecouser,findcouser,addcousse,findAll} from '../controllers/couser.js'
import {authenticateToken,authorize} from '../utils/Authorize.js'
const couser = express.Router();

couser.post('/',authenticateToken,authorize(['ADMIN']),addcousse);
couser.delete('/:id',authenticateToken,authorize(['ADMIN']),removecouser);
couser.get('/:id',authenticateToken,authorize(['ADMIN','Student', 'lecture']),findcouser);
couser.get('/',authenticateToken,authorize(['ADMIN']),findAll)



export default couser

