import express from "express";
import {
  update,
  findAll,
  addword,
  removeword,


 
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
word.delete("/:id", authenticateToken, authorize(["ADMIN", "user"]), removeword);
// word.get("/jk/:id", authenticateToken, authorize(["ADMIN", "user"]),findword);
word.get("/words", authenticateToken, authorize(["ADMIN", "user"]), findAll);
word.patch("/:id", authenticateToken, authorize(["ADMIN", "user"]), update);
// word.get('/',loginword);
// word.get(
//   "/l",
//   authenticateToken,
//   authorize(["ADMIN", "Student"]),
//   protectedRouteHandler
// );

export default word;
