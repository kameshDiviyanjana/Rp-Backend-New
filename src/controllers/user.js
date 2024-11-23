import { makerespon } from "../utils/respon.js";
import usernew from '../models/user.js'
//import usernew from '../models/user.js'
import { adduserdb, getuserbyid, removeuserbyid } from "../services/user.js";
import {customError} from '../utils/customeError.js'
import jwt from 'jsonwebtoken'
import util from 'util'
import { log } from "console";
// const asyerrohander = (func) => {
//   return (req, res, next) => {
//       // Call the provided function and handle errors asynchronously
//       func(req, res, next).catch(error => {
//           next(error); // Pass the error to the next middleware
//       });
//   };
// };
 const asyerrohander = (func)=>{

     return (req,res,next)=>{
       func(req,res,next).catch(error=> {next(error)})
     }
   }

export const adduser = asyerrohander(async (req, res,next) => {
  const data = req.body;
 
  const user = await adduserdb(req.body);
  return makerespon({ res, data: user, message: "user added successfully" });
  // const u = req.body
  // const nex =next
  // const newOrders = (await new usernew(req.body).save()).toObject();
       
   
  //  return makerespon({
  //   res,
  //   data: newOrders,
  //   message: "All user find successfully",
  // });
})
//goable error hable avable only work this
export const finduser =asyerrohander(async (req, res,next) => {
  const userfind = await getuserbyid(req.params.id);
  return makerespon({
    res,
    data: userfind,
    message: "All user find successfully",
  });
}) 


export const removetheuser = asyerrohander(
  async (req, res,next) => {
    const removebyid = await removeuserbyid(req.params.id);
    return makerespon({
      res,
      data: removebyid,
      message: "remove user successfully",
    });
  }
)


export const loginuser = asyerrohander(
  async(req, res,next)=>{

 
  const { email, password } = req.body;


        const user = (await usernew.findOne({ email }))
        // const user = await usernew
        //   .findOne({ email })
        //   .select("-password -usertype")
        //   .exec();

        //using this many can be rectrive
        // const userjj = await usernew.find({ email });
        //  console.log(userjj)
        if (!user) {
            // return res.status(404).json({ message: "User not found" });
            const error =  new customError('User not found pleces register ',400);
                  return next(error)
        }

        const isPasswordCorrect = await user.comparePassword(password, user.password);

        if (!isPasswordCorrect) {
            // return res.status(401).json({ message: "Invalid credentials" });
            const error =  new customError('Invalid credentials chanege sername or password  ',400);
                  return next(error)
        }

        // Password is correct, proceed with login
        // Return token or any other response
        const token = jwt.sign({id:user._id,role :user.usertype},process.env.SECTRE_TOKEN,{
                expiresIn : process.env.EXPIRE_Y 
           })
        // return res.status(200).json({ message: "Login successful" ,token});
      const safeUser = {
        _id: user._id,
        username: user.usename, // Assuming "usename" is a typo for "username"
        email: user.email,
      };
        const y = { token, safeUser };
         return makerespon({ res, data: y, message: " add user fhhggkkg" });
   
   
  }
)

//  export const protect = asyerrohander(
//    async(req, res,next)=>{

//     // const texttolke =  req.headers['authorization'];

//     //  let token

//     //  if(texttolke && texttolke.startswith('bearer') ){
//     //   token = texttolke.split('')[1];

//     //   if(!token){
//     //     const error =  new customError('you  snjudd credentials ',401);
//     //     return next(error)
//     //   }
//     //  }
    
//     // const decodetoke = await util.promisify( (jwt.verify)(token,process.env.SECTRE_TOKEN))

//     //  next()
//     const authHeader = req.headers['authorization'];
//     const token = authHeader && authHeader.split(' ')[1];

//     if (!token) {
//       const error =  new customError('you  are not credentials ',401);
//          return next(error)
//     }

//     jwt.verify(token, process.env.SECTRE_TOKEN, (err, user) => {
//         if (err) {
//           console.log(err)
//           const error =  new customError('you  snjudd 11111111111111 credentials ',401);
//         return next(error)
//            // return res.sendStatus(403); // Forbidden
//         }
//         req.user = user;
//         next();
//     });
//    }
//  )

 export const authenticateToken = async (req, res, next) => {
  const authHeader = req.headers.authorization;
  const token = authHeader && authHeader.split(' ')[1];
  console.log(token)
  if (!token) {
      const error = new customError('You are not authorized.', 401);
      console.log(error)
      return next(error);
  }

  try {
      const decodedToken = await util.promisify(jwt.verify)(token, process.env.SECTRE_TOKEN);
      req.user = decodedToken; // Attach decoded token payload to the request object
      console.log(decodedToken)
      const uservailide = await usernew.findById(decodedToken.id)

      if(!uservailide){
        const error = new customError('User not valide.', 401);
       
        return next(error);
      }
    //  req.user =uservailide
      next(); // Proceed to the next middleware or route handler
    
    
  } catch (error) {
      if (error.name === 'TokenExpiredError') {
          const expiredError = new customError('JWT token has expired.', 401);
          expiredError.expiredAt = error.expiredAt; // Add expiredAt information to the error object
          console.log(error)
          return next(expiredError);
      } else {
          // Handle other JWT errors
          console.log(error)
          return next(error);
      }
  }
};

// Example route handler that requires authentication
export const protectedRouteHandler = (req, res) => {
  // Access decoded user information from request object
  const  username  = req.user.role;
  res.send(`Hello, ${username}! You have accessed the protected route.`);
};

export const authorize = (requiredRoles) => {
  return (req, res, next) => {
    const userRoles = req.user.role; // Assuming roles are stored in the user object
      // Check if the user has any of the required roles
      const isAuthorized = requiredRoles.some(role => userRoles.includes(role));
      // const isAuthorized =userRoles.includes(req.user.role)
      if (!isAuthorized) {
          const error = new customError('You are not authorized to access this resource.', 403);
          return next(error);
      }

      // User has the required role(s), proceed to the next middleware or route handler
      next();
  };
};