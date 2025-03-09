import axios from "axios";
import Tools from "./Tools";

const delay_fn = (n) => new Promise(r => setTimeout(r, n));

async function getDeviceId() {
    let device_id = localStorage.getItem('device-id')
    if (device_id == null) {
        device_id = Tools.setBrowserFingerprint()
        if (!device_id) {
            await delay_fn(1000);
            device_id = localStorage.getItem('device-id')
        }
        if (!device_id) {
            device_id = localStorage.getItem('device-id')
            // location.reload();
        }
    }
    return device_id
}

const headers = {
    // 'app-version': 1,
    // 'device-type': "web",
    // 'auth-token': localStorage.getItem('auth-token'),
    // 'device-id': await getDeviceId(),
}


// let baseURL = process.env.BaseUrl

const ApiRequest = axios.create({
    baseURL: "http://localhost:8000/api/",
    timeout: 60000,
    headers: headers,
});


ApiRequest.interceptors.request.use(
    function (config) {
        return config;
    },
    function (error) {
        return Promise.reject(error);
    },
);

export default ApiRequest;