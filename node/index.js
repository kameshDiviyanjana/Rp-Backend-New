import dotenv from 'dotenv';
dotenv.config();
import express from 'express';
import cors from 'cors';
import morgan from 'morgan';
import dbconnction from './src/database/db.js';
import router from './src/routes/router.js';
import { customError } from './src/utils/customeError.js';
import { errcontro } from './src/utils/errorController.js';
import multer from 'multer';
import axios from 'axios';
import fs from 'fs';
import FormData from 'form-data';

const app = express();

app.use(express.json({ limit: "50mb" }));
app.use(express.urlencoded({ limit: "50mb" }));
app.use(express.urlencoded({ extended: true }));
app.use(morgan("dev"));
app.use('*', cors());

const upload = multer({ dest: "uploads/" });

app.post("/predict-math", upload.single("image"), async (req, res) => {
  console.log("route hit");

  if (!req.file) {
    console.log("❌ No file uploaded");
    return res.status(400).json({ error: "No image uploaded" });
  }

  try {
    console.log(`✅ Received image: ${req.file.path}`);

    const formData = new FormData();
    formData.append("image", fs.createReadStream(req.file.path));

    const response = await axios.post("http://127.0.0.1:5000/image/predict-math", formData, {
      headers: {
        ...formData.getHeaders(),
      },
    });

    console.log("✅ Flask response:", response.data);
    res.json(response.data);

    // Cleanup
    fs.unlinkSync(req.file.path);
  } catch (error) {
    console.error("❌ Error calling Flask API:", error.response?.data || error.message);
    res.status(500).json({ error: "Prediction failed", details: error.message });
  }
});

// ✅ Register your `/bs` routes AFTER `/predict-math`
app.use('/bs', router);

// ❌ This was previously blocking `/predict-math`
app.all('*', (req, res, next) => {
  const err = new customError('Custom error route', 502);
  next(err);
});

dbconnction();

app.use(errcontro);

app.use((err, req, res, next) => {
  res.status(err.status || 500);
  res.send({
    status: err.status || 500,
    message: err.message,
  });
});

const PORT = process.env.PORT || 8000;
app.listen(PORT, () => console.log(`🚀 Server running at http://localhost:${PORT}`));
