import { makerespon } from "../utils/respon.js";
import {asyerrohander} from '../utils/error.js'
import {studentenroll} from '../services/studentEnroll.js'
export const enroll = asyerrohander(async(req, res,next)=>{

     const stenroll = await studentenroll(req.body);
     return makerespon({
        res,
        data: stenroll,
        message: "All enroll successfully",
      });
})