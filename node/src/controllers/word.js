import { asyerrohander } from "../utils/error.js";
import { makerespon } from "../utils/respon.js";
import {
  removewordService,
  updatewordService,
  getAllwordsBropDownService,
  getAllwordsService,
  createwordService,
  findwordbyid,
} from "../services/word.js";
import bucket  from '../database/firebaseConfid.js'
import {PythonShell}  from 'python-shell'

export const removeword = async (req, res, next) => {
  const removebyid = await removewordService(req.body);
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


export const findbyid = asyerrohander(async (req, res, next) => {
  const user = await findwordbyid(req.params.id);
  return makerespon({ res, data: user, message: "user coures successfully" });
});


import fs from "fs";

export const Analyze = asyerrohander(async (req, res, next) => {

   const audioPath = req.file.path;

   const options = {
     mode: "text",
     pythonOptions: ["-u"], // Ensure Python uses unbuffered output
     args: [audioPath],
     env: {
       ...process.env,
       PYTHONIOENCODING: "utf-8", // Ensure UTF-8 encoding for Python output
     },
   };

   // Run the Python script
   PythonShell.run("./src/utils/analyze_audio.py", options, (err, results) => {
     if (err) {
       console.error("PythonShell error:", err);
       return res.status(500).send("Error processing audio.");
     }

     // Process the results returned by the Python script
     if (results && results.length > 0) {
       try {
         const analysisResult = results[0]; // Result from Python script
         return res.status(200).json({ message: analysisResult });
       } catch (parseError) {
         console.error("Parsing error:", parseError);
         return res.status(500).send("Failed to parse analysis results.");
       }
     } else {
       console.error("No results returned from Python script.");
       return res.status(500).send("Failed to analyze audio.");
     }
   });
});



