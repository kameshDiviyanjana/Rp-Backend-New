import speech from "../models/speeach-results.js";
import { customError } from "../utils/customeError.js";
export const labbyid = async () => {};
export const admingDleteLab = async (id) => {
  const labdelete = await lab.findByIdAndDelete({ _id: id });
  return labdelete;
};
export const findlabid = async () => {};
export const creatlabadming = async (couser) => {
  const newOrders = (await new speech(couser).save()).toObject();

  return newOrders;
};

export const admingAllLab = async () => {
  const allcouse = await speech.find();
  return allcouse;
};

export const receivelab = async (id, rserve) => {
  // const allcouse = await lab.find({_id:id},{reservaction:rserve})

  // if(!allcouse){
  //     const cousert  = await course.findByIdAndDelete(filter)
  //     return cousert
  // }else{
  //    new  customError("sorrry lab is Alery book....",401)
  // }
  // const allcouse = await lab.find({ _id: id }, { reservaction: rserve });

  //     if (allcouse.length === 1) {
  //         const cousert = await lab.findByIdAndUpdate(id);
  //         return cousert;
  //     } else {
  //         throw new customError("Sorry, the lab is already booked.", 401); // Throwing the error
  //     }

  const cousert = await speech.findByIdAndUpdate({ _id: id }, rserve);

  return cousert;
};

export const avalabelelabs = async (data) => {
  const allcouse = await speech.find({ userid: data });
  return allcouse;
};
