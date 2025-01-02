<template>
    <section class="section">
        <div class="row">
            <table class="table table-hover">
                <thead>
                    <tr>
                        <th scope="col">#</th>
                        <th scope="col">Name</th>
                        <th scope="col">URL slug</th>
                        <th scope="col">Description</th>
                        <th scope="col">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr class="info-row">
                        <td
                            v-if="showLoader"
                            colspan="5"
                            class="text-secondary"
                        >
                            <span
                                class="spinner-border spinner-border-sm"
                            ></span>
                            Fetching data...
                        </td>
                        <td
                            v-else-if="errorMsg.length > 0"
                            colspan="5"
                            class="table-danger"
                        >
                            {{ errorMsg }}
                        </td>
                        <td
                            v-else-if="topics.length == 0"
                            colspan="5"
                            class="table-secondary"
                        >
                            No data available.
                        </td>
                    </tr>
                    <tr v-for="topic in topics" :key="topic.id">
                        <th scope="row">{{ topic.id }}</th>
                        <td>{{ topic.name }}</td>
                        <td>{{ topic.slug }}</td>
                        <td>{{ topic.description }}</td>
                        <td>
                            <button
                                class="btn btn-sm btn-outline-primary"
                                @click="$emit('onActionBtnClick', 'edit', topic)"
                                data-bs-toggle="modal"
                                data-bs-target="#edit-topic-modal"
                                title="Edit"
                            >
                                <i class="bi bi-pencil-square"></i>
                            </button>
                            &nbsp;
                            <button
                                class="btn btn-sm btn-outline-danger"
                                @click="$emit('onActionBtnClick', 'delete', topic)"
                                data-bs-toggle="modal"
                                data-bs-target="#delete-topic-modal"
                                title="Delete"
                            >
                                <i class="bi bi-trash3"></i>
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </section>
</template>

<script>
import apiClient from "@/services/api/client";

export default {
    name: "DataTable",
    emits: ["onActionBtnClick"],
    data() {
        return {
            topics: [],
            showLoader: false,
            errorMsg: "",
        };
    },
    methods: {
        callTopicListAPI() {
            this.showLoader = true
            apiClient
                .get(apiClient.urls.topicList)
                .then((response) => {
                    this.topics = response.data;
                })
                .catch((error) => {
                    if (error.isNetworkIssue()) {
                        this.errorMsg = "API Server not responding";
                    } else {
                        this.errorMsg =
                            "Something went wrong while connecting API server";
                    }
                }).finally(() => {
                    this.showLoader = false
                });
        },
    },
    mounted() {
        this.callTopicListAPI();
    },
};
</script>

<style>
</style>