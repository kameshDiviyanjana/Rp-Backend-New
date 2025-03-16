import {asyerrohander} from '../utils/error.js'
import {removelabbyod,admingfindAllLabs,admingaddlab,avlablelab,reciveAvalbelHall} from '../services/lab.js' 
import { makerespon } from "../utils/respon.js";

export const labavableController = asyerrohander(async(req, res,next)=>{

     const labavlable = await avlablelab();
     return makerespon({ res, data: labavlable, message: "avable labs " });
})

  
  export const removelabcontroller = async (req, res,next) => {
    const removebyid = await removelabbyod(req.params.id);
    return makerespon({
      res,
      data: removebyid,
      message: "remove lab successfully",
    });
  };

  export const addladcontroller = asyerrohander(async(req,res,next)=>{
    const passcouser = req.body;

    const user = await admingaddlab(passcouser);
      return makerespon({ res, data: user, message: "user lab successfully" });
  }
  )


  export const findAlllab =asyerrohander(async(req,res,next)=>{

    const orders = await admingfindAllLabs();
    return makeResponse({ res, data: orders, message: 'order retrieved All successfully' });
  }) 

  export const reciveController = asyerrohander(async(req,res,next)=>{

    const labs = await reciveAvalbelHall(req.params.id, req.body);
    return makeResponse({ res, data: labs, message: 'Lad reciveController successfully' });
  })

 