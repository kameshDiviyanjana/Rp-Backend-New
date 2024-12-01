import { asyerrohander } from "../utils/error.js";
import { makerespon } from "../utils/respon.js";
import {
  removewordService,
  updatewordService,
  getAllwordsBropDownService,
  getAllwordsService,
  createwordService,

} from "../services/word.js";
import bucket  from '../database/firebaseConfid.js'


export const removeword = async (req, res, next) => {
  const removebyid = await removewordService(req.params.id);
  return makerespon({
    res,
    data: removebyid,
    message: "remove coures successfully",
  });
};

export const addword = async (req, res, next) => {
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
        const user = await createwordService({
          ...body,
          imagewordUrl: publicUrl,
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
    console.error("Unexpected error in addword:", error);
    next(error); // Pass error to error handler middleware
  }
};

// export const addword = asyerrohander(async (req, res, next) => {
//   const password = req.body;
   
//   if (!req.file) {
//     return res.status(400).send({ message: "No file uploaded" });
//   }

//   const fileName = `images/${Date.now()}_${req.file.originalname}`;
//   const file = bucket.file(fileName);

//   // Create a stream to upload the image
//   const stream = file.createWriteStream({
//     metadata: {
//       contentType: req.file.mimetype,
//     },
//   });

//   stream.on("error", (error) => {
//     console.error("Upload failed:", error);
//     res.status(500).send({ message: "Upload failed", error });
//   });

//   stream.on("finish", async () => {
//     // Make the file publicly accessible
//     await file.makePublic();
//     const publicUrl = `https://storage.googleapis.com/${bucket.name}/${fileName}`;

//     console.log("File uploaded successfully:", publicUrl);
//     res
//       .status(200)
//       .send({ message: "File uploaded successfully", url: publicUrl });
//   });

//   stream.end(req.file.buffer);
//   const user = await createwordService(password);
//   return makerespon({ res, data: user, message: "user coures successfully" });
// });

export const findAll = asyerrohander(async (req, res, next) => {
  const orders = await getAllwordsService(req.query);
  return makerespon({
    res,
    data: orders,
    message: "order retrieved All successfully",
  });
});

export const update = asyerrohander(async (req, res, next) => {
 

  const user = await updatewordService(req.params.id, req.body);
  return makerespon({ res, data: user, message: "user coures successfully" });
});
