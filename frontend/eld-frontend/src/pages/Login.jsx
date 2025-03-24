import React, {useState} from 'react';
import {Box, Button, Container, TextField, Typography} from '@mui/material';
import {LoginAPI} from "../services/Api.js";
import {toast} from "react-toastify";
import Constants from "../common/constants.js";
import {useLanding} from "../contexts/LandingContext.jsx";
import {useNavigate} from "react-router-dom";

function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const navigate = useNavigate();

    const {setIsAuth} = useLanding(); // Get login function and user state

    const handleLogin = async (e) => {
        e && e.preventDefault();
        const LoginData = {username, password};
        LoginAPI(LoginData)
            .then((response) => {
                const serverPayload = response.data;
                localStorage.setItem("access_token", serverPayload.access);
                localStorage.setItem("refresh_token", serverPayload.refresh);
                navigate(Constants.ROUTES.DASHBOARD); // Redirect to Dashboard
                setIsAuth(true);
            })
            .catch((error) => {

            });


    };

    return (
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
            <Container maxWidth="sm">
                <Typography variant="h4" align="center" gutterBottom>
                    Login
                </Typography>
                <form onSubmit={handleLogin}>
                    <TextField
                        label="Username"
                        fullWidth
                        margin="normal"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
                    <TextField
                        label="Password"
                        type="password"
                        fullWidth
                        margin="normal"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                    <Button variant="contained" color="primary" fullWidth type="submit">
                        Login
                    </Button>
                </form>
            </Container>
        </Box>
    );
}

export default Login;
