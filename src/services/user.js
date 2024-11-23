import {createuser,deleteuder,oneuserfindbyid} from '../repository/user.js'
import { default as createError } from 'http-errors';

export const adduserdb = async(data)=>{

     const addsucess = await createuser({
        ...data
     });
    
     return addsucess;
}

export const removeuserbyid = async(id)=>{
    const userremove = await deleteuder({ _id: id })
    if (!userremove) throw new createError(401, 'Invalid order ID');
    return userremove;
}

export const getuserbyid = async(id)=>{
    
    //  const oneuserfind = await oneuserfindbyid({ _id: id })
    //  if (!oneuserfind) throw new createError(401, 'Invalid order ID');
    //  return oneuserfind;
    const orders = await oneuserfindbyid(id);
    
//goable error hable avable only work this
  if (!orders) throw new createError(401, 'Invalid order ID');
  return orders;
}