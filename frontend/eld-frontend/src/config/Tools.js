class Tools {
    constructor() {
    }

    checkResponseStatus(response, successFunction, errorFunction) {

        console.log(response)

        if (response.data.status === "SUCCESS") {
            successFunction();
        } else {
            errorFunction();
        }
    }


    isProdEnv() {
        let isProd = true;
        if (process.env.NODE_ENV === "production") {
            isProd = true;
        }
        return isProd;
        //
        // let isProd = true;
        // if (process.env.NODE_ENV === "production") {
        //     isProd = true;
        // }
        // return isProd;
    }

    formData(data) {
        let formData = new FormData();
        for (let key in data) {
            formData.append(key, data[key]);
        }
        return formData;
    }

    buildGetURL(baseUrl, data) {
        const queryString = new URLSearchParams(data).toString();
        let queryParams = data ? `?${queryString}` : ""
        return `${baseUrl}${queryParams}`

    }
}

export default new Tools();