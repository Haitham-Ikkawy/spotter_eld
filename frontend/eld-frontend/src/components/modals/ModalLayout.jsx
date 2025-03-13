import React from 'react';
import {Box, Modal, Typography} from '@mui/material';
import {useLanding} from "../../contexts/LandingContext.jsx";

function ModalLayout(props) {

    const {title, modalOpened, setModalOpened, children} = props;

    const {isMobile} = useLanding(); // Get authentication state

    let mobileStyle = {
        position: "absolute",
        top: "50%",
        left: "50%",
        transform: "translate(-50%, -50%)",
        width: 300,
        bgcolor: "background.paper",
        p: 4,
        borderRadius: 2
    }
    let desktopStyle = {position: "absolute", top: "50%", left: "50%", transform: "translate(-50%, -50%)", width: 600, bgcolor: "background.paper", p: 4, borderRadius: 2}
    const boxStyle = isMobile ? mobileStyle : desktopStyle
    return (
        <Modal open={modalOpened} onClose={() => setModalOpened(false)}>
            <Box sx={boxStyle}>
                {title && <Typography variant="h6" gutterBottom>{title}</Typography>}
                {children}
            </Box>
        </Modal>
    );
}

export default ModalLayout;