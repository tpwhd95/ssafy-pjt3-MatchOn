importScripts('https://www.gstatic.com/firebasejs/7.15.0/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/7.15.0/firebase-messaging.js');

const config = {
    apiKey: "AIzaSyDGdHvQgttXEKYkihDzYhpsKc6CPavUlD4",
    authDomain: "matchon-1521d.firebaseapp.com",
    databaseURL: "https://matchon-1521d.firebaseio.com",
    projectId: "matchon-1521d",
    storageBucket: "matchon-1521d.appspot.com",
    messagingSenderId: "993144676136",
    appId: "1:993144676136:web:f6d488819130f42d4cba1d",
    measurementId: "G-B56KGDSW1X"
};

firebase.initializeApp(config);
const messaging = firebase.messaging();

// 백그라운드 상태에서 받은 알림 처리
messaging.setBackgroundMessageHandler((payload) => {
    console.log('Message received. ', payload);
    // Customize notification here
    const title = 'Background Message Title'
    const options = {
        body: payload.data.message,
        icon: '/firebase-logo.png'
    }

    return self.registration.showNotification(title, options);
});