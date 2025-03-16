import usernew from '../models/user.js'
import jwt from 'jsonwebtoken'

import {asyerrohander} from '../utils/error.js'

import {customError} from '../utils/customeError.js'
export const createuser = async(users)=>{

     // try{
          const newOrders = (await new usernew(users).save()).toObject();
          // const token = jwt.sign({id:newOrders._id,role :newOrders.usertype},process.env.SECTRE_TOKEN,{
          //      expiresIn : process.env.EXPIRE_Y 
          // })
            const safeUser = {
              _id: newOrders._id,
              username: newOrders.usename, // Assuming "usename" is a typo for "username"
              email: newOrders.email,
            };
          return safeUser;
    
   
}

export const oneuserfindbyid = async(filter)=>{

     try{

         const userfind = await usernew.findOne({_id : filter})
         if (!userfind) {
           console.log('No order found usdrr.');
            return null;
            
          }
         return userfind
     }catch(error){
        console.log(error);
     }
     
     
}

export const deleteuder = async(filter)=>{

    try{

        const muser  = await usernew.findByIdAndDelete(filter)
        if (!muser) {
            console.log('No order found with filters:', filter);
            return null;
          }
        return muser
   }catch(error){

        console.log(error)
   }
}