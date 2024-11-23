import course from '../models/course.js'

export const oneuserfindbyid = async(filter)=>{

    try{

        const userfind = await course.findOne({_id : filter})
        if (!userfind) {
          console.log('No order found usdrr.');
           return null;
           
         }
        return userfind
    }catch(error){
       console.log(error);
    }
}
export const createcouser = async(couser)=>{

    const newOrders = (await new course(couser).save()).toObject();
       
    return newOrders;
}
export const deletecouser = async(filter)=>{

//     try{

//         const cousert  = await course.findByIdAndDelete(filter)
//         if (!cousert) {
//             console.log('No couser found with filters:', filter);
//             return null;
//           }
//         return cousert
//    }catch(error){

//         console.log(error)
//    }
   const cousert  = await course.findByIdAndDelete(filter)
   return cousert
}

export const findAllcosers = async ()=>{

     const allcouse = await course.find()
     return allcouse
}
