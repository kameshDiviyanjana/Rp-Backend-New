// const  {getcouersbyid,removecousebyid,addcousedb,findAllcouser} = require('../repository/couser') 
import { getcouersbyid, removecousebyid, addcousedb, findAllcouser } from '../repository/couser';
import {removecouser,findcouser,addcousse,findAll} from '../controllers/couser.js'


jest.mock('../repository/couser.js', () => ({
    getcouersbyid: jest.fn(),
    removecousebyid: jest.fn(),
    addcousedb: jest.fn(),
 
    findAllcouser: jest.fn(),
   
  }));

  jest.mock('../utils/respon', () => ({
    makeResponse: jest.fn()
  }));

  describe('couser',()=>{

    afterEach(() => {
        jest.clearAllMocks(); // Clear mocks after each test
      });

      test('create - adds a new user and returns success response', async () => {
        const req = { body: {} };
        const res = {};
        addcousedb.mockResolvedValue('newuser');
      
        addcousse(req, res);
        expect(addcousedb).toHaveBeenCalledWith(req.body);
        expect(makeResponse).toHaveBeenCalledWith({
          res,
          data: 'newuser',
          message: 'user added successfully'
        });
      });

      test('create - adds a new user and returns success response', async () => {
        const req = { body: {} };
        const res = {};
        addcousedb.mockResolvedValue('newuser');
      
        addcousse(req, res);
        expect(addcousedb).toHaveBeenCalledWith(req.body);
        expect(makeResponse).toHaveBeenCalledWith({
          res,
          data: 'newuser',
          message: 'user added successfully'
        });
      });

      test('carete couse remove', async () => {
        const req = { body: {} };
        const res = {};
        removecousebyid.mockResolvedValue('newOrder');
      
        removecouser(req, res);
        expect(addcousedb).toHaveBeenCalledWith(req.body);
        expect(makeResponse).toHaveBeenCalledWith({
          res,
          data: 'newOrder',
          message: 'user added successfully'
        });
      });

      test('create find all couse', async () => {
        const req = { body: {} };
        const res = {};
        findAllcouser.mockResolvedValue('newuser');
      
        findcouser();
        expect(addcousedb).toHaveBeenCalledWith(req.body);
        expect(makeResponse).toHaveBeenCalledWith({
          res,
          data: 'newuser',
          message: 'user added successfully'
        });
      });

      
  })

  