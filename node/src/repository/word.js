
import { default as createError } from "http-errors";
import { words } from "../models/index.js";

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
  limit = 1,
  searchTerm,
  userme,
  pacticesword,
}) => {
  try {
    // Calculate the skip value for pagination
    const skip = (page - 1) * limit;

    // Set up the search filter to include the userme field
    const searchFilter = { userid: userme }; // assuming 'userid' is the correct field
    if (searchTerm) {
      // Use a regex search for case-insensitive matching
      searchFilter.wordAdd = { $regex: searchTerm, $options: "i" };
    }

    if (pacticesword) {
      searchFilter._id = pacticesword;
    }
    // Fetch words based on the search filter, with pagination and sorting
    const wordses = await words
      .find(searchFilter)
      .skip(skip)
      .limit(limit)
      .lean();

    // Get the total count of documents for pagination
    const totalCount = await words.countDocuments(searchFilter);
    const totalPages = Math.ceil(totalCount / limit);

    // Return the data along with pagination info
    return {
      wordses,
      totalCount,
      totalPages,
    };
  } catch (error) {
    // Log the error to help with debugging
    console.error("Error retrieving all wordses:", error);
    throw error; // Re-throw the error to be handled by the caller
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
    const { _ids } = filters; // Expecting an array of IDs to delete

    // Check if _ids is provided and is an array with at least one element
    if (!_ids || _ids.length === 0) {
      throw new Error("No IDs provided for deletion.");
    }

    // Perform the deletion operation
    const removedwordse = await words.deleteMany({
      _id: { $in: _ids }, // Match any wordse whose _id is in the _ids array
    });

    // If no documents were deleted, provide a more informative message
    if (removedwordse.deletedCount === 0) {
      return { message: "No words found matching the given IDs." };
    }

    // If deletion is successful, return the result
    return {
      message: `${removedwordse.deletedCount} words deleted successfully.`,
      deletedCount: removedwordse.deletedCount,
    };
  } catch (error) {
    // Log the error and rethrow it
    console.error("Error removing wordse:", error);
    throw error; // Optionally rethrow or wrap the error in a custom error
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

export const findword = async (id) => {
  try {
    const diet = await words.findOne(id)
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