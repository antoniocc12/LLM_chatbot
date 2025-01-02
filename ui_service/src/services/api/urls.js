import envVars from "@/services/env/vars.js"

const endPoints = {
    "token": "chatbot/token",
    "revokeToken": "chatbot/revoke-token",
    "whoami": "chatbot/whoami",
    "topicList": "chatbot/topics",
    "topicDetail": "chatbot/topics/{{topic}}",
    "datasetList": "chatbot/topics/{{topic}}/datasets",
    "taskList": "chatbot/tasks",
    "taskDetail": "chatbot/tasks/{{task_id}}",
    "query": "chatbot/topics/{{topic}}/query",
    "history": "chatbot/topics/{{topic}}/history",
}

class APIUrls {
    constructor() {
        this.token = this.generateUrl(endPoints.token)
        this.whoami = this.generateUrl(endPoints.whoami)
        this.revokeToken = this.generateUrl(endPoints.revokeToken)
        this.topicList = this.generateUrl(endPoints.topicList)
        this.topicDetail = this.generateUrl(endPoints.topicDetail)
        this.datasetList = this.generateUrl(endPoints.datasetList)
        this.taskList = this.generateUrl(endPoints.taskList)
        this.taskDetail = this.generateUrl(endPoints.taskDetail)

        this.query = this.generateUrl(endPoints.query)
        this.history = this.generateUrl(endPoints.history)
    }

    generateUrl(endPoint) {
        return this.joinPaths(envVars.VUE_APP_API_SERVER, envVars.VUE_APP_API_VERSION, endPoint);
    }

    joinPaths(...paths) {
        return paths.join("/");
    }

    replace(url, oldValue, newValue) {
        return url.replaceAll(oldValue, newValue)
    }

    getTopicDetail(topic) {
        return this.replace(this.topicDetail, "{{topic}}", topic);
    }
    getDatasetList(topic) {
        return this.replace(this.datasetList, "{{topic}}", topic);
    }
    getQuery(topic) {
        return this.replace(this.query, "{{topic}}", topic);
    }
    getHistory(topic) {
        return this.replace(this.history, "{{topic}}", topic);
    }
    getTaskDetail(taskID) {
        return this.replace(this.taskDetail, "{{task_id}}", taskID);
    }

}

export default new APIUrls()