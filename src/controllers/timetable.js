import timetable from '../models/timetable.js'
import { makerespon } from "../utils/respon.js";
import {asyerrohander} from '../utils/error.js'
import { log } from 'util';
import {savetimetable,findbydate,findBysubject} from '../services/timetable.js'
export const addtimetable = asyerrohander(

    async(req,res,next)=>{
         const passcouser = req.body;
    
        // const user = await addcousedb(passcouser);
      ///  const newOrders = (await new timetable(req.body).save()).toObject();
        // const token = jwt.sign({id:newOrders._id,role :newOrders.usertype},process.env.SECTRE_TOKEN,{
        //      expiresIn : process.env.EXPIRE_Y 
        // })
       const addsucess = await savetimetable(passcouser)
          return makerespon({ res, data: addsucess, message: "time table coures successfully" });
      }
)
//all add subject find 
export const findsubjje = asyerrohander(async (req, res,next) => {
    // try {
    //     const subjectName = req.params.subjectName;
             
    //     // Find timetable documents that contain the specified subject name in the 'module' array
    //     // const timetables = await timetable.find({' module.subject': subjectName });
    //     const timetables = await timetable.aggregate([
    //         {
    //             $match: { 'module.subject': subjectName } // Match documents containing the specified subject name in any module
    //         },
    //         {
    //             $project: {
    //                 _id: 0, // Exclude _id field from the output
    //                 modules: {
    //                     $filter: {
    //                         input: '$module',
    //                         as: 'm',
    //                         cond: { $eq: ['$$m.subject', subjectName] } // Filter modules by subject name
    //                     }
    //                 }
    //             }
    //         }
    //     ]);

    //     // Send response
    //     res.json(timetables);
    // } catch (error) {
    //     console.error('Error finding timetables by subject:', error);
    //     res.status(500).json({ error: 'An error occurred while finding timetables by subject' });
    // }
    const subjectName = await findBysubject(req.params.subjectName);
    return makerespon({ res, data: subjectName, message: "All Subject find" });

}) 


export const findbydatecontroller = async(req, res)=>{
    const datepram = await findbydate(req.params.tadate)
    // try{
    //     const date = new Date(datepram);
    //     // const timetables = await timetable.find({dates: date });
    //     // res.json(timetables);
    //      const timetables = await timetable.find({ dates: date });

    //     // Send response
    //     res.json(timetables);
    // }catch(error){
    //    console.log(error);
    // }
    return makerespon({ res, data: datepram, message: "All Subject find" });
}