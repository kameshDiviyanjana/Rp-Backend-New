import { default as createError } from "http-errors";
import {
  updatewordseRepo,

  createwordseRepo,
  findword,
} from "../repository/score.js";

export const createwordService = async (payload) => {
  try {

    const newword = await createwordseRepo({ ...payload });
    if (!newword) throw new createError(400, "Diet Type adding failed");
    return newword;
  } catch (error) {
    throw error;
  }
};


export const updatewordService = async (wordId, payload) => {
  try {

    const updatedword = await updatewordseRepo({ _id: wordId }, payload);
    if (!updatedword) throw new createError(404, "word not found");
    return updatedword;
  } catch (error) {
    throw error;
  }
};



export const findwordbyid = async (id) => {
  try {
    console.log("id", id);
    const word = await findword({ userid: id });
    if (!word) throw new createError(404, "score not found");
    return word;
  } catch (error) {
    // throw error;
    throw new createError(400, error.message);
  }
};
