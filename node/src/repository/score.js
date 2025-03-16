import { default as createError } from "http-errors";
import { score } from "../models/index.js";

const cleanwordseData = (wordse) => {
  if (wordse && wordse._doc) {
    return wordse._doc;
  }
  return null;
};

export const createwordseRepo = async (wordse) => {
  try {
    const newwordse = await new score(wordse).save();
    const cleanData = cleanwordseData(newwordse);
    return cleanData;
  } catch (error) {
   throw error;
  }
};


export const updatewordseRepo = async (filters, data) => {
  try {
    const wordse = await score.findOneAndUpdate(filters, data, {
      new: true,
    });

    if (!wordse) {
      logger.warn("No wordse found with filters:", filters);
      return null;
    }
   
    return wordse;
  } catch (error) {
  
    throw error;
  }
};

export const findword = async (id) => {
  try {
    const diet = await score.findOne(id);
    if (!diet) {
      logger.warn("No diet found with id:", id);
      return null;
    }
    // logger.info("diet retrieved:", diet);
    return diet;
  } catch (error) {
    //  logger.error("Error retrieving diet by id:", error);
    return null;
  }
};