// import { moduleLogger } from "@sliit-foss/module-logger";
import { default as createError } from "http-errors";
import { grossmotor } from "../models/index.js";

//const logger = moduleLogger("Schedule-repository");

const cleangrossmotorskillData = (grossmotorskill) => {
  if (grossmotorskill && grossmotorskill._doc) {
    return grossmotorskill._doc;
  }
  return null;
};

export const creategrossmotorskillRepo = async (grossmotorskill) => {
  try {
    const newgrossmotorskill = await new grossmotor(grossmotorskill).save();
    const cleanData = cleangrossmotorskillData(newgrossmotorskill);
   // logger.info("grossmotorskill created:", newgrossmotorskill);
    return cleanData;
  } catch (error) {
   // logger.error("Error creating grossmotorskill:", error);
    throw error;
  }
};

export const getAllgrossmotorskillsRepo = async ({
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

    const grossmotorskills = await grossmotor
      .find(searchFilter)
      .sort({ created_at: -1 })
      .skip(skip)
      .limit(limit)
      .lean();

    const totalCount = await grossmotor.countDocuments(searchFilter);
    const totalPages = Math.ceil(totalCount / limit);

    return {
      grossmotorskills,
      totalCount,
      totalPages,
    };
  } catch (error) {
    //  logger.error("Error retrieving all grossmotorskills:", error);
    throw error;
  }
};

export const getAllgrossmotorskill = async () => {
  try {
    const grossmotorskill = await grossmotor
      .find()
      .select("-created_at -updated_at")
      .collation({ locale: "en", strength: 2 })
      .sort({ wordAdd: 1 });
    return grossmotorskill;
  } catch (error) {
  //  logger.error("Error retrieving all grossmotorskills:", error);
    throw error;
  }
};

export const updategrossmotorskillRepo = async (filters, data) => {
  try {
    const grossmotorskill = await grossmotor.findOneAndUpdate(filters, data, {
      new: true,
    });

    if (!grossmotorskill) {
      logger.warn("No grossmotorskill found with filters:", filters);
      return null;
    }
    //logger.info("grossmotorskill updated:", grossmotorskill);
    return grossmotorskill;
  } catch (error) {

    throw error;
  }
};

export const removegrossmotorskillById = async (filters) => {
  try {
    const removedgrossmotorskill = await grossmotor.findOneAndDelete(filters);
    if (!removedgrossmotorskill) {
      return null;
    }
    return removedgrossmotorskill;
  } catch (error) {
    throw error;
  }
};

export const findgrossmotorskillfilter = async (id) => {
  try {
    const diet = await grossmotor.findOne(id).lean();
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
