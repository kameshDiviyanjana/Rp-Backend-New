import enroll from '../models/studentEnroll.js'
import {customError} from '../utils/customeError.js'
export const  createnroll = async(data)=>{

    const newOrders = (await new enroll(data).save()).toObject();
       
    return newOrders;
}


export const removeenroll = async(sudjectid)=>{

    const  deletes = await enroll.findByIdAndDelete({_id:sudjectid});
    if (!deletes) {
       const error = new customError('not subject ',500);
        return null;
      }
    return deletes
}