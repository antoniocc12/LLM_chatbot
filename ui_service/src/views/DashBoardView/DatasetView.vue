<template>
    <main id="main" class="main">
        <div class="pagetitle">
            <h1><i class="bi bi-file-earmark-text"></i> Dataset</h1>
            <nav>
                <ol class="breadcrumb">
                    <li class="breadcrumb-item">
                        <a href="">Home</a>
                    </li>
                    <li class="breadcrumb-item active">Dataset</li>
                </ol>
            </nav>

            <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                <div v-if="errorMsg.length > 0" class="col-lg-8 col-md-6 col-sm-12">
                    <span class="text-danger">{{errorMsg}}</span>
                </div>
                <div class="col-lg-3 col-md-4 col-sm-12">
                    <div v-if="showLoader" class="loader-container">
                        <span class="spinner-border spinner-border-sm"></span>
                    </div>
                    <select
                        class="form-select form-select-sm"
                        v-model="selectedTopic"
                    >
                        <option
                            v-for="topic in topics"
                            :key="topic.id"
                            :value="topic.slug"
                        >
                            {{ topic.name }}
                        </option>
                    </select>
                </div>
                <button
                    class="btn btn-sm btn-primary"
                    type="button"
                    data-bs-toggle="modal"
                    data-bs-target="#add-dataset-modal"
                >
                    <i class="bi bi-plus-circle"></i> Add
                </button>
            </div>
        </div>
        <modal-add :topics="topics" :selected-topic="selectedTopic" @on-dataset-add="onDatasetAdd" />
        <data-table v-if="topicsAvailable" :topics="topics" :selected-topic="selectedTopic" ref="datasetDataTable" />
    </main>
</template>

<script>
import ModalAdd from "@/components/ui/dataset/ModalAdd.vue";
import apiClient from "@/services/api/client";
import DataTable from "@/components/ui/dataset/DataTable.vue"

export default {
    name: "DatasetView",
    components: {
        ModalAdd,
        DataTable,
    },
    data() {
        return {
            topics: [],
            selectedTopic: "",
            showLoader: false,
            errorMsg: "",
            topicsAvailable: false
        };
    },
    methods: {
        callTopicListAPI() {
            this.showLoader = true;
            apiClient
                .get(apiClient.urls.topicList)
                .then((response) => {
                    this.topics = response.data;
                    if (this.topics.length > 0) {
                        this.selectedTopic = this.topics[0].slug
                        this.topicsAvailable = true
                    }
                })
                .catch((error) => {
                    if (error.isNetworkIssue()) {
                        this.errorMsg = "API Server not responding";
                    } else {
                        this.errorMsg =
                            "Something went wrong while connecting API server";
                    }
                })
                .finally(() => {
                    this.showLoader = false;
                });
        },
        onDatasetAdd() {
            this.$refs.datasetDataTable.callDatasetListAPI();
        }
    },
    created() {
        this.callTopicListAPI();
    },
};
</script>

<style scoped>
div:has(> .loader-container) {
    position: relative;
}
.loader-container {
    position: absolute;
    left: 7px;
    top: 5px;
}
</style>