<template>
    <div
        class="modal fade"
        id="add-dataset-modal"
        tabindex="-1"
        aria-labelledby="addDatasetModalLabel"
        aria-hidden="true"
    >
        <div class="modal-dialog">
            <div class="modal-content">
                <form @submit.prevent="submitForm">
                    <div class="modal-header">
                        <h1 class="modal-title fs-5" id="addDatasetModalLabel">
                            Add Dataset for <span class="fw-bold">{{ topic.name }}</span>
                        </h1>
                        <button
                            type="button"
                            class="btn-close"
                            data-bs-dismiss="modal"
                            aria-label="Close"
                        ></button>
                    </div>
                    <div class="modal-body">
                        <div class="form-group">
                            <label for="fileDataset" class="form-label"
                                >Dataset file</label
                            >
                            <input
                                @change="onFileChange"
                                ref="fileInput"
                                class="form-control"
                                type="file"
                                id="formFile"
                            />
                        </div>
                        <alert-box
                            v-if="errorMsg.length > 0"
                            :msg="errorMsg"
                            @close="errorMsg = ''"
                        />
                    </div>
                    <div class="modal-footer">
                        <button
                            ref="closeModal"
                            type="button"
                            class="btn btn-secondary"
                            data-bs-dismiss="modal"
                        >
                            Close
                        </button>
                        <button type="submit" class="btn btn-primary">
                            <span
                                v-if="showLoader"
                                class="spinner-border spinner-border-sm"
                            ></span
                            >Upload Dataset
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import apiClient from "@/services/api/client";
import AlertBox from "@/components/ui/AlertBox.vue";

export default {
    name: "ModalAdd",
    props: ["topics", "selectedTopic"],
    components: { AlertBox },
    emits: ["onDatasetAdd"],
    data() {
        return {
            formData: {
                file: null,
            },
            showLoader: false,
            errorMsg: "",
            topic: {
                name: "Unknown...",
            },
        };
    },
    methods: {
        showError(error) {
            this.errorMsg = error;
        },
        clearForm() {
            this.$refs.fileInput.value = null;
            this.formData.file = null;
        },
        onFileChange(event) {
            this.formData.file = event.target.files[0];
        },
        updateTopicName() {
            for (let index in this.topics) {
                if (this.selectedTopic === this.topics[index].slug) {
                    this.topic.name = this.topics[index].name;
                    return;
                }
            }
            this.topic.name = "Unknown";
        },
        submitForm() {
            this.showLoader = true;
            apiClient
                .post(apiClient.urls.getDatasetList(this.selectedTopic), new apiClient.typeCast.ToFormData(this.formData))
                // eslint-disable-next-line no-unused-vars
                .then((response) => {
                    this.clearForm();
                    this.$refs.closeModal.click();
                    this.$emit("onDatasetAdd");
                })
                .catch((error) => {
                    if (error.isNetworkIssue()) {
                        this.showError("API Server not responding");
                    } else {
                        if (error.response.status == 400) {
                            this.showError(JSON.stringify(error.response.data));
                        } else {
                            this.showError(
                                "Something went wrong. Check the logs."
                            );
                        }
                    }
                })
                .finally(() => {
                    this.showLoader = false;
                });
        },
    },
    mounted() {
        this.updateTopicName();
    },
    watch: {
        // eslint-disable-next-line no-unused-vars
        selectedTopic(newValue) {
            this.updateTopicName();
        },
    },
};
</script>

<style>
</style>