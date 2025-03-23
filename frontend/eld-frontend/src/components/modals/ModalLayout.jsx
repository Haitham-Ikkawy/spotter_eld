import React from 'react';
import { Box, Modal, Typography, IconButton } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import { useLanding } from "../../contexts/LandingContext.jsx";

function ModalLayout({ title, modalOpened, setModalOpened, children }) {
    const { isMobile } = useLanding();

    const boxStyle = {
        position: "absolute",
        top: "50%",
        left: "50%",
        transform: "translate(-50%, -50%)",
        width: isMobile ? 300 : 600,
        bgcolor: "background.paper",
        p: 4,
        borderRadius: 2,
        boxShadow: 24
    };

    const handleClose = (event, reason) => {
        if (reason !== "backdropClick") {
            setModalOpened(false);
        }
    };

    return (
        <Modal open={modalOpened} onClose={handleClose}>
            <Box sx={boxStyle}>
                <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                    {title && <Typography variant="h6">{title}</Typography>}
                    <IconButton onClick={() => setModalOpened(false)} size="small">
                        <CloseIcon />
                    </IconButton>
                </Box>
                {children}
            </Box>
        </Modal>
    );
}

export default ModalLayout;
