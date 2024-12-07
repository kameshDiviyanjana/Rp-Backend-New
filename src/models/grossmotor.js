import mongoose from "mongoose";

const grossmotormodle = new  mongoose.Schema(

    {
        grossmotorskill: {
            type : String,
            required : [true,'Gross motor name is require']
        },
        grossmotorcode : {
            type : String,
            required : [true,'Gross motor code is require']
        },
        description :{
            type : String,
            required : [true,'Gross motor description is require']
        },
        url : {
            type : String
        }

    }
)

const grossmotor  = mongoose.model('Grossmotor',grossmotormodle)

export default grossmotor