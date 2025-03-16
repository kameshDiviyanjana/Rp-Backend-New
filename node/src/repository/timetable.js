import timetable from '../models/timetable.js'


export const timetableaddrepositer = async(data)=>{

    const newOrders = (await new timetable(data).save()).toObject();

    return newOrders
}


export const findbydaterepositer = async(data)=>{

    try{
        const date = new Date(data);
        // const timetables = await timetable.find({dates: date });
        // res.json(timetables);
         const timetables = await timetable.find({ dates: date });

        // Send response
     //   res.json(timetables);

     return timetables
    }catch(error){
       console.log(error);
    }
       
}

export const findbysubjectrepositer = async(data)=>{

    try {
        const subjectName = data;
             
        // Find timetable documents that contain the specified subject name in the 'module' array
        // const timetables = await timetable.find({' module.subject': subjectName });
        const timetables = await timetable.aggregate([
            {
                $match: { 'module.subject': subjectName } // Match documents containing the specified subject name in any module
            },
            {
                $project: {
                    _id: 0, // Exclude _id field from the output
                    modules: {
                        $filter: {
                            input: '$module',
                            as: 'm',
                            cond: { $eq: ['$$m.subject', subjectName] } // Filter modules by subject name
                        }
                    }
                }
            }
        ]);

        // Send response
      //  res.json(timetables);

        return timetables
    } catch (error) {
        console.error('Error finding timetables by subject:', error);
        res.status(500).json({ error: 'An error occurred while finding timetables by subject' });
    }
       
}


