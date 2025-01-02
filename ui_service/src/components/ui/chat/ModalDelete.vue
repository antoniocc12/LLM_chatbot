<template>
    <div
        class="modal fade"
        id="delete-chat-history-modal"
        tabindex="-1"
        aria-labelledby="deleteChatHistoryModalLabel"
        aria-hidden="true"
    >
        <div class="modal-dialog">
            <div class="modal-content">
                <form @submit.prevent="submitForm">
                    <div class="modal-header">
                        <h1 class="modal-title fs-5" id="deleteChatHistoryModalLabel">
                            Confirm deletion
                        </h1>
                        <button
                            type="button"
                            class="btn-close"
                            data-bs-dismiss="modal"
                            aria-label="Close"
                        ></button>
                    </div>
                    <div class="modal-body">
                        <p>Are you sure want to delete the chat history?</p>
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
                        <button type="submit" class="btn btn-danger">
                            <span
                                v-if="showLoader"
                                class="spinner-border spinner-border-sm"
                            ></span
                            >Yes
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
    name: "ModalDelete",
    props: ["topic"],
    emits: ["onHistoryDelete"],
    components: { AlertBox },
    data() {
        return {
            showLoader: false,
            errorMsg: "",
        };
    },
    methods: {
        showError(error) {
            this.errorMsg = error;
        },
        submitForm() {
            let topicSlug = null;
            if (this.topic) {
                topicSlug = this.topic.slug;
            }
            this.showLoader = true;
            apiClient
                .delete(apiClient.urls.getHistory(topicSlug))
                // eslint-disable-next-line no-unused-vars
                .then((response) => {
                    this.$refs.closeModal.click();
                    this.$emit("onHistoryDelete");
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
                            console.log(error);
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