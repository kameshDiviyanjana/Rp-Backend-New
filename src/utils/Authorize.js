import usernew from '../models/user.js'
import {customError} from '../utils/customeError.js'
import jwt from 'jsonwebtoken'
import util from 'util'


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