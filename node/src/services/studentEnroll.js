import {createnroll} from '../repository/studentEnroll.js'
export const studentenroll = async(data)=>{

      const stunetesenroll = await createnroll({

        ...data
      })

      return stunetesenroll;
}

