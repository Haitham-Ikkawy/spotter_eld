import {LandingContextProvider} from "./contexts/LandingContext.jsx";

import {ToastContainer} from "react-toastify";
import AppWrapper from "./components/shared/AppWrapper.jsx";

function App() {
    return (

        <LandingContextProvider>
            <ToastContainer autoClose={3000} closeOnClick/>
            <AppWrapper/>
        </LandingContextProvider>
    );
}

export default App;