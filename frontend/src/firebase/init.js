import firebase from 'firebase/app';
import firestore from 'firebase/firestore';

var config = {
  apiKey: "AIzaSyDGdHvQgttXEKYkihDzYhpsKc6CPavUlD4",
  authDomain: "matchon-1521d.firebaseapp.com",
  databaseURL: "https://matchon-1521d.firebaseio.com",
  projectId: "matchon-1521d",
  storageBucket: "matchon-1521d.appspot.com",
  messagingSenderId: "993144676136",
  appId: "1:993144676136:web:f6d488819130f42d4cba1d",
  measurementId: "G-B56KGDSW1X"
};
// Initialize Firebase
const firebaseApp = firebase.initializeApp(config);
firebaseApp.firestore().settings({ timestampInSnapshots: true });

export default firebaseApp.firestore();