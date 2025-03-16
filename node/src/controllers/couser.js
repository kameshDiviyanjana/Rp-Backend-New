import {asyerrohander} from '../utils/error.js'
import { makerespon } from "../utils/respon.js";
import {getcouersbyid,removecousebyid,addcousedb,findAllcouser} from '../services/couser.js'

export const findcouser = asyerrohander(async (req, res,next) => {

  const userfind = await getcouersbyid(req.params.id);
  
  return makerespon({
    res,
    data: userfind,
    message: "All coures find successfully",
  });
})
  
  export const removecouser = async (req, res,next) => {
    const removebyid = await removecousebyid(req.params.id);
    return makerespon({
      res,
      data: removebyid,
      message: "remove coures successfully",
    });
  };

  export const addcousse = asyerrohander(async(req,res,next)=>{
    
    const passcouser = req.body;

    const user = await addcousedb(passcouser);
      return makerespon({ res, data: user, message: "user coures successfully" });
  }

 
  )


  export const findAll =asyerrohander(async(req,res,next)=>{

    const orders = await findAllcouser(req.query);
    return makeResponse({ res, data: orders, message: 'order retrieved All successfully' });
  }) 