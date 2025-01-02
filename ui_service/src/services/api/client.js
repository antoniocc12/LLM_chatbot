import axios from "axios";
import apiUrls from "./urls"


class APIClientError {
    constructor(error) {
        this.code = error.code;
        this.message = error.message;
        this.response = this.getResponse(error);
    }

    getResponse(error) {
        let errorResponse = null;
        if (error.response) {
            errorResponse = error.response;
        }
        return errorResponse;
    }

    isNetworkIssue() {
        return this.code === "ERR_NETWORK";
    }
}

class ToFormData {
    constructor(data) {
        this.data = data;
    }

    typeCast() {
        const data = new FormData();
        for (let field in this.data) {
            data.append(field, this.data[field]);
        }
        return data;
    }
}

class APIClient {
    constructor() {
        // Supported datatypes
        this.typeCast = { ToFormData };

        this.tokenType = "Bearer";
        this.accessToken = null;
        this.refreshToken = null;

        this.defaultConfig = {};
        this.activeConfig = {};

        this.urls = apiUrls
    }

    setTokens(tokenResponse) {
        this.accessToken = tokenResponse.access_token;
        this.refreshToken = tokenResponse.refresh_token;
        this.tokenType = tokenResponse.token_type;
    }

    clearTokens() {
        this.accessToken = null;
        this.refreshToken = null;
        this.tokenType = "Bearer";
    }

    processData(data) {
        if (data.constructor.name === this.typeCast.ToFormData.name) {
            data = data.typeCast();
            this.addHeader("Content-Type", "multipart/form-data");
        }
        return data
    }

    addHeader(name, value) {
        if (!("headers" in this.activeConfig)) {
            this.activeConfig.headers = {}
        }
        this.activeConfig.headers[name] = value
    }

    attachAuthCredentials() {
        if (this.accessToken !== null) {
            this.addHeader("Authorization", `${this.tokenType} ${this.accessToken}`)
        }
    }

    request() {
        this.attachAuthCredentials()

        const config = this.activeConfig

        return new Promise(function (resolve, reject) {
            axios(config)
                .then(function (response) {
                    resolve(response)
                })
                .catch(function (error) {
                    if (error.response) {
                        if (error.response.status == 401) {
                            // TODO: Implement token end-point call with refresh token.
                            reject(new APIClientError(error))
                        } else {
                            reject(new APIClientError(error))
                        }
                    }
                    else {
                        reject(new APIClientError(error))
                    }
                })
        });
    }

    get(url, config = {}) {
        this.activeConfig = { ...this.defaultConfig, ...config }
        this.activeConfig.url = url
        this.activeConfig.method = "get"

        return this.request()
    }

    delete(url, config = {}) {
        this.activeConfig = { ...this.defaultConfig, ...config }
        this.activeConfig.url = url
        this.activeConfig.method = "delete"

        return this.request()
    }

    post(url, data = null, config = {}) {
        this.activeConfig = { ...this.defaultConfig, ...config }
        this.activeConfig.url = url
        this.activeConfig.method = "post"

        if (data !== null) {
            this.activeConfig.data = this.processData(data)
        }

        return this.request()
    }

    put(url, data = null, config = {}) {
        this.activeConfig = { ...this.defaultConfig, ...config }
        this.activeConfig.url = url
        this.activeConfig.method = "put"

        if (data !== null) {
            this.activeConfig.data = this.processData(data)
        }

        return this.request()
    }

    patch(url, data = null, config = {}) {
        this.activeConfig = { ...this.defaultConfig, ...config }
        this.activeConfig.url = url
        this.activeConfig.method = "patch"

        if (data !== null) {
            this.activeConfig.data = this.processData(data)
        }

        return this.request()
    }
}

const apiClient = new APIClient()

export default apiClient; 