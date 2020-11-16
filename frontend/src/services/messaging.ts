import { ref } from '@vue/composition-api';
import firebase from 'firebase/app';
import 'firebase/messaging';
import config from '../../../firebaseConfig';

firebase.initializeApp(config);

const token = ref<string>('');
const messaging = firebase.messaging();
messaging.usePublicVapidKey('BFkC_RJgJiV2-FZ5I2sdG5ifkhETUKFhl-QDgJPB5dttB39gSThZMkuey-O-QubiXi1oLYlk1maylCWMF47TjYQ');

messaging.getToken().then((currentToken) => {
    if (currentToken) {
        console.log(currentToken);
        token.value = currentToken;
    } else {
        // Show permission request.
        console.log('No Instance ID token available. Request permission to generate one.');
    }
});
messaging.onMessage((payload) => {
    console.log(payload);
    const title = 'Title';
    const options = {
        body: payload.data.message,
        icon: '/firebase-logo.png',
    };
    const notification = new Notification(title, options);
    return notification;
});

export {
    token,
    messaging,
};