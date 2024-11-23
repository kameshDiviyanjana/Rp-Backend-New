import {oneuserfindbyid,deletecouser,createcouser,findAllcosers} from '../repository/couser.js'
export const getcouersbyid = async(id)=>{

    const coures = await oneuserfindbyid(id);
    if (!coures) throw new createError(401, 'Invalid order ID');
    return coures;
}
export const removecousebyid = async(id)=>{
    const userremove = await deletecouser({ _id: id })
    return userremove;
}
export const addcousedb = async(data)=>{
    const addcoures = await createcouser({
        ...data
     });
    
     return addcoures;
}
export const findAllcouser =async(query)=>{
    
    findAllcosers(query)
}