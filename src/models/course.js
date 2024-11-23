import mongoose from "mongoose";

const coursemodle = new  mongoose.Schema(

    {
        coursename: {
            type : String,
            required : [true,'couser  Name is require']
        },
        cousercode : {
            type : String,
            required : [true,'couser  code is require']
        },
        description :{
            type : String,
            required : [true,'couser  description is require']
        },
        credite : {
         type : Number,
         required : [true,'couser  credit is require']
        }

    }
)

const course  = mongoose.model('Course',coursemodle)

export default course