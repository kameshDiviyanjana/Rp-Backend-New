import { asyerrohander } from "../utils/error.js";
import { makerespon } from "../utils/respon.js";
import {
  updatewordService,
  createwordService,
  findwordbyid,
} from "../services/socre.js";



 export const addword = asyerrohander(async (req, res, next) => {
   const passcouser = req.body;

   const user = await createwordService(passcouser);
   return makerespon({ res, data: user, message: "user coures successfully" });
 });


export const update = asyerrohander(async (req, res, next) => {
  const user = await updatewordService(req.params.id, req.body);
  return makerespon({ res, data: user, message: "user coures successfully" });
});

export const findbyid = asyerrohander(async (req, res, next) => {
  const user = await findwordbyid(req.params.id);
  return makerespon({ res, data: user, message: "user coures successfully" });
});


