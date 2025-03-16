import express from 'express';
import {labavableController,removelabcontroller,addladcontroller,findAlllab,reciveController} from '../controllers/lab.js'
import {authenticateToken,authorize} from '../utils/Authorize.js'

const lab = express.Router();

lab.post('/add',authenticateToken,authorize(['ADMIN']),addladcontroller);
lab.get('/avlable',authenticateToken,authorize(['ADMIN']),labavableController);
lab.delete('/:id',authenticateToken,authorize(['ADMIN']),removelabcontroller);
lab.patch('/:id',authenticateToken,authorize(['ADMIN']), reciveController);
lab.get('/All',authenticateToken,authorize(['ADMIN']),findAlllab)
//user.get('/l',authenticateToken,authorize(['ADMIN','Student']),protectedRouteHandler);

export default lab