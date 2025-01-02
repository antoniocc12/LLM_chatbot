<template>
    <section class="section">
        <div class="row">
            <table class="table table-hover">
                <thead>
                    <tr>
                        <th scope="col">#</th>
                        <th scope="col">Name</th>
                        <th scope="col">Task ID</th>
                        <th scope="col">Status</th>
                        <th scope="col">Current state</th>
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
                            v-else-if="datasets.length == 0"
                            colspan="5"
                            class="table-secondary"
                        >
                            No data available.
                        </td>
                    </tr>
                    <data-table-row v-for="dataset in datasets" :key="dataset.id" :dataset="dataset" />
                </tbody>
            </table>
        </div>
    </section>
</template>

<script>
import apiClient from "@/services/api/client";
import DataTableRow from './DataTableRow.vue';

export default {
    name: "DataTable",
    props: ["topics", "selectedTopic"],
    components: {
        DataTableRow
    },
    data() {
        return {
            datasets: [],
            showLoader: false,
            errorMsg: "",
        };
    },
    methods: {
        callDatasetListAPI() {
            this.showLoader = true
            this.datasets = []
            apiClient
                .get(apiClient.urls.getDatasetList(this.selectedTopic))
                .then((response) => {
                    this.datasets = response.data;
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
        this.callDatasetListAPI();
    },
    watch: {
        // eslint-disable-next-line no-unused-vars
        selectedTopic(newValue) {
            this.callDatasetListAPI()
        }
    }
};
</script>

<style>
</style>