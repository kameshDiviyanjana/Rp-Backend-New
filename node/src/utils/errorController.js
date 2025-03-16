// export const errcontro  = (error,req,res,next)=>{
//    error.statusCode = err && err.statusCode ? err.statusCode : 500;
//    error.status =  error.status || 'error';
//     res.status(error.statusCode).json({
//         status:error.statusCode,
//         massage : error.massage
//     })
// }

// errorController.js

export const errcontro = (error, req, res, next) => {
    // const statusCode = error && error.statusCode ? error.statusCode : 500;
    // const status = error.status || 'error';
    // res.status(statusCode).json({
    //     status: status,
    //     message: error.message // Corrected typo here
    // });
    const statusCode = error && error.statusCode ? error.statusCode : 500;
    const statuss = error && error.status ? error.status : 'error'; // Check if status property exists
    const message = error && error.message ? error.message : 'Internal Server Error'; // Provide default message
    
    res.status(statusCode).json({
                status:statusCode,
                massage : message,
               
           })
           
};
