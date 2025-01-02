<template>
    <div
        class="modal fade"
        id="add-topic-modal"
        tabindex="-1"
        aria-labelledby="addTopicModalLabel"
        aria-hidden="true"
    >
        <div class="modal-dialog">
            <div class="modal-content">
                <form @submit.prevent="submitForm">
                    <div class="modal-header">
                        <h1 class="modal-title fs-5" id="addTopicModalLabel">
                            Add Topic/Knowledge
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
                            <label for="inputTopic">Knowledge/Topic</label>
                            <input
                                v-model="formData.name"
                                type="text"
                                class="form-control"
                                id="inputTopic"
                                placeholder="Example: N4 TOS, AIML Framework"
                            />
                        </div>
                        <div class="form-group">
                            <label for="inputTopicDescription"
                                >Description</label
                            >
                            <textarea
                                v-model="formData.description"
                                class="form-control"
                                id="inputTopicDescription"
                                rows="3"
                                placeholder="About the topic"
                            ></textarea>
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
                            >Add Topic
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
    components: {AlertBox},
    emits: ["onTopicAdd"],
    data() {
        return {
            formData: {
                name: "",
                description: "",
            },
            showLoader: false,
            errorMsg: "",
        };
    },
    methods: {
        showError(error) {
            this.errorMsg = error;
        },
        clearForm() {
            this.formData.name = "";
            this.formData.description = "";
        },
        submitForm() {
            this.showLoader = true;
            apiClient
                .post(apiClient.urls.topicList, this.formData)
                // eslint-disable-next-line no-unused-vars
                .then((response) => {
                    this.clearForm();
                    this.$refs.closeModal.click();
                    this.$emit("onTopicAdd")
                })
                .catch((error) => {
                    if (error.isNetworkIssue()) {
                        this.showError("API Server not responding");
                    } else {
                        if (error.response.status == 400) {
                            this.showError(JSON.stringify(error.response.data))
                        }else {
                            this.showError("Something went wrong. Check the logs.");
                            console.log(error)
                        }
                    }
                })
                .finally(() => {
                    this.showLoader = false;
                });
        },
    },
};
</script>

<style>
</style>