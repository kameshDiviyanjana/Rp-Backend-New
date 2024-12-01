//Import the functions you need from the SDKs you need

// import admin from "irebase-admin";
// import serviceAccount from "./serviceAccountKey.json";
// admin.initializeApp({
//   credential: admin.credential.cert(serviceAccount),
//   storageBucket: "your-project-id.appspot.com", // Replace with your storage bucket URL
// });

// export const bucket = admin.storage().bucket();
import admin from "firebase-admin"; // Correct spelling: "firebase-admin"
import serviceAccount from "./serviceAccountKey.json" assert { type: "json" };

// Initialize Firebase Admin SDK
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  storageBucket: "gs://imageuplode-3e802.appspot.com", // Replace with your Firebase Storage bucket URL
});

// Export the bucket for use in other files
 const bucket = admin.storage().bucket();

export default bucket;


