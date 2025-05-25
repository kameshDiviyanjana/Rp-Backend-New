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
import { progressRoutes } from './src/routes/progressRoutes.js';
import languagePreferenceRoutes from './src/routes/languagePreferenceRoutes.js';

const app = express();

app.use(express.json({ limit: "50mb" }));
app.use(express.urlencoded({ limit: "50mb" }));
app.use(express.urlencoded({ extended: true }));
app.use(morgan("dev"));
app.use('*', cors());

const upload = multer({ dest: "uploads/" });

app.use("/api/progress", progressRoutes);
app.use('/api/language-preferences',languagePreferenceRoutes );
app.use('/bs', router);

//  This was previously blocking `/predict-math`
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
