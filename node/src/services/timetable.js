import {timetableaddrepositer,findbydaterepositer,findbysubjectrepositer} from '../repository/timetable.js'


export const savetimetable = async(data)=>{
    const addtimetable = await timetableaddrepositer(
        {
            ...data
        }
        
      
       )
    
       return addtimetable;
}


export const findbydate = async(data)=>{
    const finddatasucess = await findbydaterepositer(data)

    return finddatasucess
}

export const findBysubject = async(data)=>{
   
    const sudject = await findbysubjectrepositer(data)
       return sudject;
}
