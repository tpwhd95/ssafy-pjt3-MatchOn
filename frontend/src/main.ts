import firebase from 'firebase/app'
import 'firebase/messaging'

const firebaseConfig = {
    apiKey: "AIzaSyDGdHvQgttXEKYkihDzYhpsKc6CPavUlD4",
    authDomain: "matchon-1521d.firebaseapp.com",
    databaseURL: "https://matchon-1521d.firebaseio.com",
    projectId: "matchon-1521d",
    storageBucket: "matchon-1521d.appspot.com",
    messagingSenderId: "993144676136",
    appId: "1:993144676136:web:f6d488819130f42d4cba1d",
    measurementId: "G-B56KGDSW1X"
};

firebase.initializeApp(firebaseConfig)

const messaging = firebase.messaging()

messaging.usePublicVapidKey('BFkC_RJgJiV2-FZ5I2sdG5ifkhETUKFhl-QDgJPB5dttB39gSThZMkuey-O-QubiXi1oLYlk1maylCWMF47TjYQ')

// 알림 수신을 위한 사용자 권한 요청
Notification.requestPermission()
    .then((permission) => {
        console.log('permission ', permission)
        if (permission !== 'granted') {
            alert('알림을 허용해주세요')
        }
    })

// TODO: Send token to server for send notification
messaging.getToken()
    .then(console.log)

// Handle received push notification at foreground
messaging.onMessage(payload => {
    console.log(payload)
    alert(payload.data.message)
})