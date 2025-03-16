// import mongoose from "mongoose";
// import bcrypt  from 'bcryptjs'
// const user = new  mongoose.Schema(

//     {
//         usename: {
//             type : String,
//             required : [true,'usename is require']
//         },
//         email : {
//             type : String,
//             required : [true,'email is require']
//         },
//         password :{
//             type : String,
//             required : [true,'password is required ']
//         },
//         confirmPassword : {
//               type :String,
//               required : [true,'confirmpassword is required '],
//               validate:{
//                  validator: function(val){

//                     return val == this.password;

//                  },
//                  message : 'password & not confirem '
//               }
//         },
//         usertype : {
//             type: String,
//       enum : ['ADMIN', 'Student','lecture'],
//       default: 'Student'
//         }

//     }
// )

// user.pre('save',async function(next) {

//     if(!this.isModified('password')) return next();
    
//    this.password =await bcrypt.hash(this.password,12);
   
//    this.confirmPassword = undefined;
//   next();
// })

// user.methods.comparePassword  = async function(pswd,pswdDb){

//   return  await bcrypt.compare(pswd,pswdDb)
// }

// const usernew  = mongoose.model('Users',user)

// export default usernew
import mongoose from "mongoose";
import bcrypt from 'bcryptjs';

const userSchema = new mongoose.Schema({
  usename: {
    type: String,
    required: [true, "usename is require"],
  },
  email: {
    type: String,
    required: [true, "email is require"],
  },
  password: {
    type: String,
    required: [true, "password is required "],
  },
  confirmPassword: {
    type: String,
    required: [true, "confirmpassword is required "],
    validate: {
      validator: function (val) {
        return val === this.password;
      },
      message: "password & not confirem",
    },
  },
  usertype: {
    type: String,
    enum: ["ADMIN", "user", "lecture"],
    default: "user",
  },
});

userSchema.pre('save', async function(next) {
    if (!this.isModified('password')) return next();
    this.password = await bcrypt.hash(this.password, 12);
    this.confirmPassword = undefined;
    next();
});

userSchema.methods.comparePassword = async function(pswd, pswdDb) {
    return await bcrypt.compare(pswd, pswdDb);
};

const usernew = mongoose.model('Users', userSchema);

export default usernew;
