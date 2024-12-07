import { default as createError } from "http-errors";
import {
  findgrossmotorskillfilter,
  removegrossmotorskillById,
  updategrossmotorskillRepo,
  getAllgrossmotorskill,
  getAllgrossmotorskillsRepo,
  creategrossmotorskillRepo,
} from "../repository/grossmotor.js";

export const creategrossmotorskillService = async (payload) => {
  try {
    // const diet = await findgrossmotorskillfilter({ grossmtorskillAdd: payload.grossmtorskillAdd });
    // if (diet)
    //   throw new createError(
    //     400,
    //     `The grossmtorskillAdd name is already in use. Please Enter a different grossmtorskillAdd name.`
    //   );
    const newgrossmtorskill = await creategrossmotorskillRepo({ ...payload });
    if (!newgrossmtorskill) throw new createError(400, "Diet Type adding failed");
    return newgrossmtorskill;
  } catch (error) {
    throw error;
  }
};

export const getAllgrossmotorskillsService = async (query) => {
  let { page, limit, searchTerm, userme } = query;
  page = parseInt(page, 10) || 1;
  limit = parseInt(limit, 10) || 10;
  searchTerm = searchTerm || "";

  try {
    const grossmtorskill = await getAllgrossmotorskillsRepo({ page, limit, searchTerm, userme });
    return grossmtorskill;
  } catch (error) {
    throw new createError(500, "Error getting grossmtorskills");
  }
};

export const getAllgrossmotorskillDropDownService = async () => {
  try {
    const grossmtorskill = await getAllgrossmotorskill();
    return grossmtorskill;
  } catch (error) {
    throw new createError(500, "Error getting grossmtorskills");
  }
};

export const updategrossmotorskillService = async (grossmtorskillId, payload) => {
  try {
    const diet = await findgrossmotorskillfilter({
      _id: { $ne: grossmtorskillId },
      diet_type: payload.grossmtorskillAdd,
    });
    if (diet)
      throw new createError(
        400,
        `The diet name is already in use. Please Enter a different diet name.`
      );
    const updatedgrossmtorskill = await updategrossmotorskillRepo(
      { _id: grossmtorskillId },
      payload
    );
    if (!updatedgrossmtorskill) throw new createError(404, "grossmtorskill not found");
    return updatedgrossmtorskill;
  } catch (error) {
    throw error;
  }
};

export const removegrossmotorskillService = async (id) => {
  try {
    const grossmtorskill = await removegrossmotorskillById({ _id: id });
    if (!grossmtorskill) throw new createError(404, "grossmtorskill not found");
    return grossmtorskill;
  } catch (error) {
    // throw error;
    throw new createError(400, error.message);
  }
};
