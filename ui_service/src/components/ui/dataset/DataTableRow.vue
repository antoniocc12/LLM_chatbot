<template>
    <tr>
        <th scope="row">{{ datasetObj.id }}</th>
        <td>{{ datasetObj.name }}</td>
        <td>{{ datasetObj.task.task_id }}</td>
        <td :class="[statusClass()]">
            <span
                v-if="showLoader"
                class="spinner-border spinner-border-sm"
            ></span>
            <span class="fw-normal">{{ datasetObj.task.status }}</span>
        </td>
        <td>{{ datasetObj.task.current_state }}</td>
    </tr>
</template>

<script>
import apiClient from "@/services/api/client";

export default {
    name: "DataTableRow",
    props: ["dataset"],
    data() {
        return {
            trace: {
                enabled: true,
                interval: 5,
                terminateStatuses: ["SUCCESS", "ERROR", "ERROR_NETWORK"],
            },
            datasetObj: this.dataset,
            showLoader: false,
            timeOut: null,
        };
    },
    methods: {
        traceStatusChange() {
            if (
                !this.trace.terminateStatuses.includes(
                    this.datasetObj.task.status
                )
            ) {
                this.showLoader = true;
                this.timeOut = setTimeout(this.callTaskDetailAPI, this.trace.interval * 1000);
            } else {
                this.showLoader = false;
            }
        },

        callTaskDetailAPI() {
            const taskId = this.datasetObj.task.task_id;
            apiClient
                .get(apiClient.urls.getTaskDetail(taskId))
                .then((response) => {
                    this.datasetObj.task.status = response.data.status;
                    this.datasetObj.task.current_state =
                        response.data.current_state;
                    this.traceStatusChange();
                })
                .catch((error) => {
                    if (error.isNetworkIssue()) {
                        this.datasetObj.task.status = "ERROR_NETWORK";
                    } else {
                        this.datasetObj.task.status = "ERROR";
                    }
                    this.showLoader = false;
                });
        },

        statusClass() {
            const statusClassMapper = {
                PENDING: "text-secondary",
                STARTED: "text-primary",
                SUCCESS: "text-success",
                ERROR: "text-danger",
                ERROR_NETWORK: "text-danger",
            };
            return statusClassMapper[this.datasetObj.task.status];
        },
    },
    mounted() {
        if (this.trace.enabled) {
            this.traceStatusChange();
        }
    },
    unmounted() {
        clearTimeout(this.timeOut);
    },
};
</script>

<style>
</style>