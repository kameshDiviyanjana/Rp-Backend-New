import express from "express";

import {
  update,
  addword,
  findbyid,
} from "../controllers/score.js";
import multer from "multer";
const score = express.Router();


import {
  authenticateToken,
  authorize,
  protectedRouteHandler,
} from "../utils/Authorize.js";
score.post("/", authenticateToken, authorize(["ADMIN", "user"]), addword);
score.patch("/:id", authenticateToken, authorize(["ADMIN", "user"]), update);
score.get("/:id", authenticateToken, authorize(["ADMIN", "user"]), findbyid);


export default score;
