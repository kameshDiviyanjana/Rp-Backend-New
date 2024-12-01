import { default as createError } from "http-errors";
import {
  findwordsefilter,
  removewordseById,
  updatewordseRepo,
  getAllwordses,
  getAllwordsesRepo,
  createwordseRepo,
} from "../repository/word.js";

export const createwordService = async (payload) => {
  try {
    const diet = await findwordsefilter({ wordAdd: payload.wordAdd });
    if (diet)
      throw new createError(
        400,
        `The wordAdd name is already in use. Please Enter a different wordAdd name.`
      );
    const newword = await createwordseRepo({ ...payload });
    if (!newword) throw new createError(400, "Diet Type adding failed");
    return newword;
  } catch (error) {
    throw error;
  }
};

export const getAllwordsService = async (query) => {
  let { page, limit, searchTerm, userme } = query;
  page = parseInt(page, 10) || 1;
  limit = parseInt(limit, 10) || 10;
  searchTerm = searchTerm || "";

  try {
    const words = await getAllwordsesRepo({ page, limit, searchTerm, userme });
    return words;
  } catch (error) {
    throw new createError(500, "Error getting words");
  }
};

export const getAllwordsBropDownService = async () => {
  try {
    const words = await getAllwordses();
    return words;
  } catch (error) {
    throw new createError(500, "Error getting words");
  }
};

export const updatewordService = async (wordId, payload) => {
  try {
    const diet = await findwordsefilter({
      _id: { $ne: wordId },
      diet_type: payload.wordAdd,
    });
    if (diet)
      throw new createError(
        400,
        `The diet name is already in use. Please Enter a different diet name.`
      );
    const updatedword = await updatewordseRepo(
      { _id: wordId },
      payload
    );
    if (!updatedword) throw new createError(404, "word not found");
    return updatedword;
  } catch (error) {
    throw error;
  }
};

export const removewordService = async (id) => {
  try {
    const word = await removewordseById({ _id: id });
    if (!word) throw new createError(404, "word not found");
    return word;
  } catch (error) {
    // throw error;
    throw new createError(400, error.message);
  }
};
