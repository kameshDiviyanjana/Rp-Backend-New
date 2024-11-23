import dotenv from 'dotenv';
dotenv.config()
import express from 'express'
import cors from 'cors'
import morgan from 'morgan'
import dbconnction from './database/db.js'
import router from './routes/router.js'
import {customError} from './utils/customeError.js'
import {errcontro} from './utils/errorController.js'
const app = express()

app.use(express.json({ limit: "50mb" }));
app.use(express.urlencoded({ limit: "50mb" }));
//app.use(express.urlencoded({ extended: true }))
app.use("*", cors());
app.use(morgan("dev"));
app.use('*',
    cors()
);

app.use('/bs',router)
app.all('*',(req,res,next)=>{

  const err=new customError('customerruo rouet',502);
  next(err)
})
dbconnction()
app.use((req, res, next) => {
    next(createError.NotFound);
  });

  app.use(errcontro)
  
  app.use((err, req, res, next) => {
    res.status(err.status || 500);
    res.send({
      status: err.status || 500,
      message: err.message,
    });
  });
console.log(process.env.PORT );
const PORT = process.env.PORT || 8000;
app.listen(PORT, () => console.log(`🚀 @ http://localhost:${PORT}`));