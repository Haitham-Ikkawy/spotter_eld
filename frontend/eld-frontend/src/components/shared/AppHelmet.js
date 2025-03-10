import React from "react";
import {Helmet} from "react-helmet";

function AppHelmet() {

    return (
        <Helmet>
            <meta charSet="utf-8"/>
            <title>Eld App</title>
            {/*<meta property="og:title" content={title}/>*/}
            {/*<meta property="og:description" content={description}/>*/}
            {/*<meta*/}
            {/*    property="og:image:secure_url"*/}
            {/*    content={image}*/}
            {/*/>*/}
            {/*<meta property="og:url" content={window.location.href}/>*/}
            <meta name="description" lang="en" content={description}/>
            <meta property="og:type" content="website"/>
            <link rel="icon" href="../../assets/images/favicon.png"/>
        </Helmet>
    );
}

export default AppHelmet;
