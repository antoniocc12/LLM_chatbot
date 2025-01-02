class Url {
    constructor() {
        this.url = new URL(window.location.href);
        this.searchParams = this.url.searchParams;
        this.appModes = {
            plugin: "plugin",
            web: "web",
        };
        this.topics = {
            all: "__all__",
        };
    }

    getSearchParamAppMode() {
        return (this.searchParams.get("appMode") || this.appModes.web).toLowerCase();
    }

    getSearchParamTopic() {
        return (this.searchParams.get("topic") || this.topics.all).toLowerCase();
    }

    isAppModeWeb() {
        return this.getSearchParamAppMode() === this.appModes.web;
    }

    isAppModePlugin() {
        return this.getSearchParamAppMode() === this.appModes.plugin;
    }

    isTopicAll() {
        return this.getSearchParamTopic() === this.topics.all;
    }


}

export default new Url()