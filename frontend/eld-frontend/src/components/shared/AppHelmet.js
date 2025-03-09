import React, {useContext} from "react";
import {Helmet} from "react-helmet";
import {LandingContext} from "../../contexts/LandingContext";

function AppHelmet() {

    const {serverPageConfig} = useContext(LandingContext);

    const title = serverPageConfig?.page_title ? serverPageConfig?.page_title : "";

    const favicon = serverPageConfig?.favicon_url ? serverPageConfig?.favicon_url : "";
    // const description = "NumAds is a platform where you can subscribe to your favorite services and get the latest news and updates.";
    const description = "";

    const image = "https://numads.com/assets/images/numads.png";
    return (
        <Helmet>
            <meta charSet="utf-8"/>
            <title>{title}</title>
            <meta property="og:title" content={title}/>
            <meta property="og:description" content={description}/>
            <meta
                property="og:image:secure_url"
                content={image}
            />
            <meta property="og:url" content={window.location.href}/>
            <meta name="description" lang="en" content={description}/>
            <meta property="og:type" content="website"/>
            <link rel="icon" href={favicon}/>
        </Helmet>
    );
}

export default AppHelmet;
