
// export const asyerrohander = (func)=>{

//      return (req,res,next)=>{
//        func(req,res,next).catch(error=> {next(error)})
//      }
// }

export const asyerrohander = (func) => {
    return (req, res, next) => {
        func(req, res, next).catch((err)=>{
          next(err)
        });
    }
}
