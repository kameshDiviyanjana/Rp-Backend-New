//  import dotenv from 'dotenv';
//   dotenv.config();
import mongoose  from 'mongoose'
//  console.log("MongoDB URI:", process.env.MONGO_URL)
const dbconnction =  async()=>{
      
    mongoose.set('strictQuery', true);
     try{

        const connect = await mongoose.connect(process.env.MONGO_URL)
        if(connect){
            console.log("connected sucessfull mongo ")
           
        }
     
     }catch(error){

        
         console.log("MONGO nOT conneted")
         console.log(error)
         console.error(error);
     }
    
}

export default dbconnction