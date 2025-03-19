import { default as createError } from 'http-errors';

import {
  avalabelelabs,
  admingDleteLab,
  creatlabadming,
  admingAllLab,
  receivelab,
  findlastrow,
} from "../repository/lab.js";


export const removelabbyod = async(query)=>{
   const {id} = query;
    const dlete=await admingDleteLab(id) 
    return dlete
}

export const admingfindAllLabs = async()=>{
   
  const lab = await admingAllLab()
  if (!lab) throw new createError(401, 'Invalid order ID');
    return lab
   

}
export const admingaddlab = async(data)=>{
    
   const succeslab = await creatlabadming(
    {
        ...data
    }
    
  
   )

   return succeslab;
}

export const avlablelab = async(data)=>{
   const {id} = data
    const labsavalab = await avalabelelabs(id);
    if (!labsavalab) throw new createError(401, 'labs Not Avalbele');
    return labsavalab;
    
}

export const lastresyltserives = async (data) => {
  const { id } = data;
  const labsavalab = await findlastrow(id);
  if (!labsavalab) throw new createError(401, "labs Not Avalbele");
  return labsavalab;
};

export const  reciveAvalbelHall = async(id,data)=>{

     const recive = await receivelab(id,data);

     return recive;
}