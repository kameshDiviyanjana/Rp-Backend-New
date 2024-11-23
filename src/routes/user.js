import express from 'express';
import {adduser,finduser,removetheuser,protectedRouteHandler,authenticateToken,authorize} from '../controllers/user.js'
const user = express.Router();
//import {authenticateToken,authorize} from '../utils/Authorize.js'
user.post('/',adduser);
user.delete('/:id',removetheuser);
 user.get('/jk/:id',authenticateToken,finduser);
// user.get('/',loginuser);
user.get('/l',authenticateToken,authorize(['ADMIN','Student']),protectedRouteHandler);


export default user