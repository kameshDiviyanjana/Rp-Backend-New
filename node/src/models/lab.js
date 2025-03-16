import mongoose from "mongoose";

const labmodul = new  mongoose.Schema(

    {
        labnumber: {
            type : String,
            required : [true,'couser  Name is require']
        },
        time : {
            type : Date,
            required : [true,'couser  code is require']
        },
        date :{
            type : String,
            required : [true,'couser  description is require']
        },
        location :{
            type : String,
            required : [true,'couser  description is require']
        },
        reservaction :{
            type: String,
            enum: ['R','N'],
            default: 'N'
        }
       

    }
)

const lab  = mongoose.model('Lab',labmodul)

export default lab