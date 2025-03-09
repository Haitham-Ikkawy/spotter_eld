import React from "react";
import {Typography} from "@mui/material";

const PageTitle = (props) => {

    const {title} = props
    return (
        <Typography variant="h4" gutterBottom sx={{mt: 2, mb:2}}>
            {title}
        </Typography>
    );
};

export default PageTitle;
