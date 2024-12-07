import express from "express";
import {
  update,
  findAll,
  addgrossmotorskill,
  removegrossmotorskill,


 
} from "../controllers/grossmotor.js";
import multer from "multer";
const grossmotorskill = express.Router();
const storage = multer.memoryStorage();
const upload = multer({ storage });
import {
  authenticateToken,
  authorize,
  protectedRouteHandler,
} from "../utils/Authorize.js";
grossmotorskill.post(
  "/",
  authenticateToken,
  authorize(["ADMIN", "user"]),upload.single("image"),
  addgrossmotorskill
);
grossmotorskill.delete("/:id", authenticateToken, authorize(["ADMIN", "user"]), removegrossmotorskill);

grossmotorskill.get("/grossmotorskill", authenticateToken, authorize(["ADMIN", "user"]), findAll);
grossmotorskill.patch("/:id", authenticateToken, authorize(["ADMIN", "user"]), update);


export default grossmotorskill;
