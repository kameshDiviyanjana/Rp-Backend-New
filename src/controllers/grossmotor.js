import { asyerrohander } from "../utils/error.js";
import { makerespon } from "../utils/respon.js";
import {
  removegrossmotorskillService,
  updategrossmotorskillService,
  getAllgrossmotorskillDropDownService,
  getAllgrossmotorskillsService,
  creategrossmotorskillService,

} from "../services/grossmotor.js";
import bucket  from '../database/firebaseConfid.js'


export const removegrossmotorskill = async (req, res, next) => {
  const removebyid = await removegrossmotorskillService(req.params.id);
  return makerespon({
    res,
    data: removebyid,
    message: "remove gross motor skill successfully",
  });
};

export const addgrossmotorskill = async (req, res, next) => {
  try {
    const { body } = req;

    if (!req.file) {
      return res.status(400).json({ message: "No file uploaded" });
    }

    const fileName = `images/${Date.now()}_${req.file.originalname}`;
    const file = bucket.file(fileName);

    const stream = file.createWriteStream({
      metadata: {
        contentType: req.file.mimetype,
      },
    });

    stream.on("error", (error) => {
      console.error("Upload failed:", error);
      return res.status(500).json({ message: "Upload failed", error });
    });

    stream.on("finish", async () => {
      try {
        await file.makePublic();
        const publicUrl = `https://storage.googleapis.com/${bucket.name}/${fileName}`;

        console.log("File uploaded successfully:", publicUrl);
        const user = await creategrossmotorskillService({
          ...body,
          url: publicUrl,
        });
        return makerespon({
          res,
          data: user,
          message: "File and user added successfully",
          url: publicUrl,
        });
      } catch (error) {
        console.error("Error making file public:", error);
        return res.status(500).json({ message: "Error finalizing upload" });
      }
    });

    stream.end(req.file.buffer);
  } catch (error) {
    console.error("Unexpected error in addgrossmotorskill:", error);
    next(error); // Pass error to error handler middleware
  }
};


export const findAll = asyerrohander(async (req, res, next) => {
  const orders = await getAllgrossmotorskillsService(req.query);
  return makerespon({
    res,
    data: orders,
    message: "order retrieved All successfully",
  });
});

export const update = asyerrohander(async (req, res, next) => {
 

  const user = await updategrossmotorskillService(req.params.id, req.body);
  return makerespon({ res, data: user, message: "Update gross motor skill successfully" });
});
