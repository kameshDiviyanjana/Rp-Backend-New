import mongoose from "mongoose";

const StudntEnrollmodul = new  mongoose.Schema(

    {
        studentid: {
            type: String,
            required: [true, 'Day is required'],
            unique: true
        },
       studentname : {
        type: String,
        required : [true,'couser  description is require'],
        
    
       },
     
        Enrollmodule : [
            {
                subject: {
                    type : String,
                    required : [true,'subject  Name is require']
                },
                subjectcode : {
                    type : String,
                    required : [true,'subjectcode  code is require']
                },
                year:{
                    type : String,
                    required : [true,'year is require']
                },
                idofsubject : {
                    type : String,
                    required : [true,'idofsubject is require']
                }
            }
        ]
    }
)

const enroll  = mongoose.model('Enroll',StudntEnrollmodul)

export default enroll