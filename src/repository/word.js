// import { moduleLogger } from "@sliit-foss/module-logger";
import { default as createError } from "http-errors";
import { words } from "../models/index.js";

//const logger = moduleLogger("Schedule-repository");

const cleanwordseData = (wordse) => {
  if (wordse && wordse._doc) {
    return wordse._doc;
  }
  return null;
};

export const createwordseRepo = async (wordse) => {
  try {
    const newwordse = await new words(wordse).save();
    const cleanData = cleanwordseData(newwordse);
   // logger.info("wordse created:", newwordse);
    return cleanData;
  } catch (error) {
   // logger.error("Error creating wordse:", error);
    throw error;
  }
};

export const getAllwordsesRepo = async ({
  page = 1,
  limit = 10,
  searchTerm,
  userme,
}) => {
  try {
    const skip = (page - 1) * limit;

    // const searchFilter = {};
    const searchFilter = { userid: userme };
    if (searchTerm) {
      searchFilter.wordAdd = { $regex: searchTerm, $options: "i" };
    }

    const wordses = await words
      .find(searchFilter)
      .sort({ created_at: -1 })
      .skip(skip)
      .limit(limit)
      .lean();

    const totalCount = await words.countDocuments(searchFilter);
    const totalPages = Math.ceil(totalCount / limit);

    return {
      wordses,
      totalCount,
      totalPages,
    };
  } catch (error) {
    //  logger.error("Error retrieving all wordses:", error);
    throw error;
  }
};

export const getAllwordses = async () => {
  try {
    const wordses = await words
      .find()
      .select("-created_at -updated_at")
      .collation({ locale: "en", strength: 2 })
      .sort({ wordAdd: 1 });
    return wordses;
  } catch (error) {
  //  logger.error("Error retrieving all wordses:", error);
    throw error;
  }
};

export const updatewordseRepo = async (filters, data) => {
  try {
    const wordse = await words.findOneAndUpdate(filters, data, {
      new: true,
    });

    if (!wordse) {
      logger.warn("No wordse found with filters:", filters);
      return null;
    }
    //logger.info("wordse updated:", wordse);
    return wordse;
  } catch (error) {
   // logger.error("Error updating wordse:", error);
    throw error;
  }
};

export const removewordseById = async (filters) => {
  try {
    // const count = await Menu.countDocuments({ wordse: filters._id });

    // if (count > 0) {
    //   logger.warn(
    //     "Cannot delete wordse because it is still being referenced in Menu documents:",
    //     filters
    //   );
    //   throw new Error(
    //     "Cannot delete wordse because it is still being referenced in Menu documents."
    //   );
    // }
    const removedwordse = await words.findOneAndDelete(filters);
    if (!removedwordse) {
    //  logger.warn("No wordse found with filters:", filters);
      return null;
    }
   // logger.info("wordse removed:", removedwordse);
    return removedwordse;
  } catch (error) {
  //  logger.error("Error removing wordse:", error);
    throw error;
  }
};

export const findwordsefilter = async (id) => {
  try {
    const diet = await words.findOne(id).lean();
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
