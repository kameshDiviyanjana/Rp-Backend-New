//Import the functions you need from the SDKs you need

// import admin from "irebase-admin";
// import serviceAccount from "./serviceAccountKey.json";
// admin.initializeApp({
//   credential: admin.credential.cert(serviceAccount),
//   storageBucket: "your-project-id.appspot.com", // Replace with your storage bucket URL
// });

// export const bucket = admin.storage().bucket();
// import admin from "firebase-admin"; 
// //import assert from "assert";
// // Correct spelling: "firebase-admin"
// import serviceAccount from "./serviceAccountKey.json" assert { type: "json" };

// // Initialize Firebase Admin SDK
// admin.initializeApp({
//   credential: admin.credential.cert({
//     type: process.env.FIRBASR_TYPE,
//     project_id: process.env.FIRBASR_ID,
//     private_key_id: process.env.FIRBASR_PRIVATE,
//     private_key: process.env.FIRBASR_PRIVATE_KEY,

//     client_email: process.env.FIRBASR_CLIENT_EMAIL,

//     client_id: process.env.FIRBASR_CLIENT_ID,
//     auth_uri: process.env.FIRBASR_AUTH,
//     token_uri: process.env.FIRBASR_ROKEN_URL,
//     auth_provider_x509_cert_url: process.env.FIRBASR_AUTH_PROVIDER,
//     client_x509_cert_url: process.env.FIRBASR_CLIENT,
//     universe_domain: process.env.FIRBASR_UNIVERSEL,
//   }),
//   storageBucket: "gs://imageuplode-3e802.appspot.com", // Replace with your Firebase Storage bucket URL
// });

// // Export the bucket for use in other files
//  const bucket = admin.storage().bucket();

// export default bucket;
import dotenv from "dotenv";
dotenv.config();
import admin from "firebase-admin";


// Initialize Firebase Admin SDK
admin.initializeApp({
  credential: admin.credential.cert({
    type: process.env.FIREBASE_TYPE, // Corrected variable names
    project_id: process.env.FIREBASE_PROJECT_ID,
    private_key_id: process.env.FIREBASE_PRIVATE_KEY_ID,
    private_key: process.env.FIREBASE_PRIVATE_KEY?.replace(/\\n/g, "\n"), // Ensures multiline keys are handled correctly
    client_email: process.env.FIREBASE_CLIENT_EMAIL,
    client_id: process.env.FIREBASE_CLIENT_ID,
    auth_uri: process.env.FIREBASE_AUTH_URI,
    token_uri: process.env.FIREBASE_TOKEN_URI,
    auth_provider_x509_cert_url: process.env.FIREBASE_AUTH_PROVIDER_CERT_URL,
    client_x509_cert_url: process.env.FIREBASE_CLIENT_CERT_URL,
    universe_domain: process.env.FIREBASE_UNIVERSE_DOMAIN,
  }),
  storageBucket: "gs://imageuplode-3e802.appspot.com", // Replace with your Firebase Storage bucket URL
});

// Export the bucket for use in other files
const bucket = admin.storage().bucket();

export default bucket;


