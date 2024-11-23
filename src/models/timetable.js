import mongoose from "mongoose";

const timetablemobul = new  mongoose.Schema(

    {
        day: {
            type: String,
          
            required: [true, 'Day is required']
        },
       dates : {
        type : Date,
       
        required : [true,'couser  description is require'],
        unique: true,
      
    
       },
     
        module : [
            {
                subject: {
                    type : String,
                    required : [true,'subject  Name is require']
                },
                subjectcode : {
                    type : String,
                    required : [true,'subjectcode  code is require']
                },hallNumber :{
                    type : String,
                    required : [true,'hallNumber  description is require']
                },
                time :{
                    type : String,
                    required : [true,'couser  description is require']
                }
            }
        ]

    }
)

const timetable  = mongoose.model('Timetable',timetablemobul)

export default timetable