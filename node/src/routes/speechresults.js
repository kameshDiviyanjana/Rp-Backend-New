import express from "express";
import {
  labavableController,
  removelabcontroller,
  addladcontroller,
  findAlllab,
  reciveController,
  lastresults,
} from "../controllers/lab.js";
import { authenticateToken, authorize } from "../utils/Authorize.js";

const sppechresults = express.Router();

sppechresults.post(
  "/add",
  authenticateToken,
 authorize(["ADMIN", "user"]),
  addladcontroller
);
sppechresults.get(
  "/avlable",
  authenticateToken,
  authorize(["ADMIN", "user"]),
  labavableController
);
sppechresults.get(
  "/last-results",
  authenticateToken,
  authorize(["ADMIN", "user"]),
  lastresults
);
sppechresults.delete(
  "/:id",
  authenticateToken,
 authorize(["ADMIN", "user"]),
  removelabcontroller
);
sppechresults.patch(
  "/:id",
  authenticateToken,
 authorize(["ADMIN", "user"]),
  reciveController
);
sppechresults.get("/All", authenticateToken,authorize(["ADMIN", "user"]), findAlllab);
//user.get('/l',authenticateToken,authorize(['ADMIN','Student']),protectedRouteHandler);

export default sppechresults;
