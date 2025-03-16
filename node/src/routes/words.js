import express from "express";
import path from "path";

import {
  update,
  findAll,
  addword,
  removeword,
  Analyze,
  findbyid,
} from "../controllers/word.js";
import multer from "multer";
const word = express.Router();
const storage = multer.memoryStorage();
const upload = multer({ storage });

import {
  authenticateToken,
  authorize,
  protectedRouteHandler,
} from "../utils/Authorize.js";
word.post(
  "/",
  authenticateToken,
  authorize(["ADMIN", "user"]),upload.single("image"),
  addword
);
word.post("/deleteword", authenticateToken, authorize(["ADMIN", "user"]), removeword);
word.get("/words", authenticateToken, authorize(["ADMIN", "user"]), findAll);
word.patch("/:id", authenticateToken, authorize(["ADMIN", "user"]), update);
word.get("/:id", authenticateToken, authorize(["ADMIN", "user"]), findbyid);
word.post(
  "/analyze",
  authenticateToken,
  authorize(["ADMIN", "user"]),
  upload.single("audio"),
  Analyze
);



export default word;
