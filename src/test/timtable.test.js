import {addtimetable,findsubjje,findbydate} from '../controllers/timetable.js'

jest.mock('../repository/couser.js', () => ({
    getcouersbyid: jest.fn(),
    removecousebyid: jest.fn(),
    addcousedb: jest.fn(),
 
    findAllcouser: jest.fn(),
   
  }));

  jest.mock('../utils/respon', () => ({
    makeResponse: jest.fn()
  }));