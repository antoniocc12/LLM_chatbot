<template>
    <main ref="chatWindow" id="main" class="main">
        <div class="pagetitle">
            <h1><i class="bi bi-chat"></i> Chat</h1>
            <nav>
                <ol class="breadcrumb">
                    <li class="breadcrumb-item">
                        <a href="">Home</a>
                    </li>
                    <li class="breadcrumb-item active">Chat</li>
                    <li v-if="showLoader" class="breadcrumb-item active">
                        <span class="spinner-border spinner-border-sm"></span>
                    </li>
                    <li v-if="selectedTopic" class="breadcrumb-item active">
                        {{ selectedTopic.name }}
                        <i
                            v-if="showTopicCloseButton"
                            @click="
                                selectedTopic = null;
                                errorMsg = '';
                            "
                            title="Close the chat."
                            class="bi bi-x-circle icon-breadcrumb"
                        ></i>
                        <i
                            v-if="messages.length > 0"
                            title="Clear the chat history."
                            class="bi bi-trash icon-breadcrumb"
                            data-bs-toggle="modal"
                            data-bs-target="#delete-chat-history-modal"
                        ></i>
                    </li>
                </ol>
            </nav>
        </div>
        <section class="section pb-5">
            <div v-if="selectedTopic === null" class="row">
                <div v-if="errorMsg.length > 0" class="info text-danger">
                    {{ errorMsg }}
                </div>
                <div v-else-if="topics.length === 0" class="info text-secondary">
                    No knowledge/topic available...
                </div>
                <div
                    v-for="topic in topics"
                    :key="topic.id"
                    class="col-lg-4 col-md-6 col-sm-12"
                >
                    <div class="card" @click="selectedTopic = topic">
                        <div class="card-body">
                            <h5 class="card-title">{{ topic.name }}</h5>
                            <p
                                v-if="topic.description == ''"
                                class="text-muted"
                            >
                                No description
                            </p>
                            <p v-else>{{ topic.description }}</p>
                        </div>
                    </div>
                </div>
            </div>
            <div v-else>
                <div class="row justify-content-center" ref="chatBoxContainer">
                    <chat-box
                        v-for="(message, index) in messages"
                        :key="index"
                        :msg="message.message"
                        :msgFrom="message.from"
                        :msgMeta="message.metadata"
                    />
                    <chat-box
                        v-if="showTyping"
                        msg="./cmd.showTyping"
                        msgFrom="jarvis"
                    />
                    <chat-box
                        v-if="chatErrorMsg.length > 0"
                        :msg="chatErrorMsg"
                        msgFrom="jarvis"
                    />
                </div>
            </div>
        </section>
    </main>
    <chat-bar v-if="selectedTopic !== null" @on-query-submit="onQuerySubmit" />
    <modal-delete :topic="selectedTopic" @on-history-delete="onHistoryDelete" />
</template>

<script>
import apiClient from "@/services/api/client";
import url from "@/services/utils/url";
import ChatBar from "@/components/ui/chat/ChatBar.vue";
import ChatBox from "@/components/ui/chat/ChatBox.vue";
import ModalDelete from "@/components/ui/chat/ModalDelete.vue";

export default {
    name: "ChatView",
    components: {
        ChatBar,
        ChatBox,
        ModalDelete,
    },
    data() {
        return {
            showLoader: false,
            showTyping: false,
            errorMsg: "",
            chatErrorMsg: "",
            topics: [],
            selectedTopic: null,
            messages: [],
            query: "",
            showTopicCloseButton: true
        };
    },
    methods: {
        callTopicListAPI() {
            this.showLoader = true;
            apiClient
                .get(apiClient.urls.topicList)
                .then((response) => {
                    this.topics = response.data;
                    if (!url.isTopicAll()) {
                        let topicSelectedFromUrl = url.getSearchParamTopic();
                        this.showTopicCloseButton = false;
                        for (let index in this.topics) {
                            if (topicSelectedFromUrl == this.topics[index].slug) {
                                this.selectedTopic = this.topics[index];
                                break;
                            }
                        }
                        if (this.selectedTopic == null) {
                            this.errorMsg = `Selected topic(${topicSelectedFromUrl}) not found`;
                            this.topics = []
                        }
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
        callHistoryAPI() {
            this.showLoader = true;
            apiClient
                .get(apiClient.urls.getHistory(this.selectedTopic.slug))
                .then((response) => {
                    this.pushMessagesFromHistoryResponse(response.data);
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
        callQueryAPI() {
            this.showTyping = true;
            this.chatErrorMsg = "";
            this.$nextTick(() => {
                this.scrollChatWindowToBottom();
            });
            apiClient
                .post(apiClient.urls.getQuery(this.selectedTopic.slug), {
                    query: this.query,
                })
                .then((response) => {
                    if (response.data["answer"] === null) {
                        this.chatErrorMsg =
                            "./cmd.showError:Chat service is down.";
                        return;
                    }
                    this.pushMessage(
                        "jarvis",
                        this.processAnswer(response.data["answer"]),
                        response.data["metadata"]
                    );
                })
                .catch((error) => {
                    if (error.isNetworkIssue()) {
                        this.chatErrorMsg =
                            "./cmd.showError:API Server not responding";
                    } else {
                        if (error.response.status === 401) {
                            this.chatErrorMsg =
                                "./cmd.showError:ERROR: Authorization  failed. Please login.";
                        } else if (error.response.status === 400) {
                            if (error.response.data.detail) {
                                this.chatErrorMsg =
                                    "./cmd.showError:ERROR: " +
                                    error.response.data.detail;
                            } else {
                                this.chatErrorMsg =
                                    "./cmd.showError:ERROR: " +
                                    JSON.stringify(error.response.data);
                            }
                        } else {
                            this.chatErrorMsg =
                                "./cmd.showError:Something went wrong while connecting API server";
                        }
                    }
                })
                .finally(() => {
                    this.showTyping = false;
                });
        },
        pushMessagesFromHistoryResponse(histories) {
            this.messages = [];
            for (let index in histories) {
                let history = histories[index];
                this.pushMessage("user", history["query"], null, false);
                this.pushMessage("jarvis", history["answer"], history["metadata"], false);
            }
            this.$nextTick(() => {
                this.scrollChatWindowToBottom();
            });
        },
        pushMessage(user, message, metadata = null, enableScrolling = true) {
            this.messages.push({
                from: user,
                message: message,
                metadata: metadata,
            });
            if (enableScrolling) {
                this.$nextTick(() => {
                    this.scrollChatWindowToBottom();
                });
            }
        },
        onQuerySubmit(query) {
            this.query = query;
            this.pushMessage("user", this.query);
            this.callQueryAPI();
        },
        onHistoryDelete() {
            this.messages = [];
            this.chatErrorMsg= "";
        },
        scrollChatWindowToBottom() {
            const container = this.$refs.chatBoxContainer;
            if (container.children.length > 0) {
                const el = container.children[container.children.length - 1];
                el.scrollIntoView({ behavior: "smooth" });
            }
        },
        processAnswer(answer) {
            return answer.replaceAll("\n", "<br />");
        },
    },
    mounted() {
        this.callTopicListAPI();
    },
    watch: {
        selectedTopic(newValue) {
            this.messages = [];
            this.showTyping = false;
            this.chatErrorMsg = "";
            if (newValue !== null) {
                this.callHistoryAPI();
            }
        },
    },
};
</script>

<style scoped>
.card {
    cursor: pointer;
}
.card:hover {
    box-shadow: 0px 0 10px rgb(42, 61, 239, 0.2);
    border: solid 1px rgb(230, 228, 228);
}
.icon-breadcrumb {
    cursor: pointer;
    margin: 0px 3px;
    padding: 0px 3px;
    color: rgba(108, 117, 125, 1);
}
.icon-breadcrumb.bi-x-circle:hover {
    color: rgba(33, 37, 41, 1);
}
.icon-breadcrumb.bi-trash:hover {
    color: rgba(220, 53, 69, 1);
}

.chat-messages {
    display: flex;
    flex-direction: column;
    max-height: 800px;
    overflow-y: scroll;
}

.chat-message-left,
.chat-message-right {
    display: flex;
    flex-shrink: 0;
}

.chat-message-left {
    margin-right: auto;
}

.chat-message-right {
    flex-direction: row-reverse;
    margin-left: auto;
}

.btn-breadcrumb {
    padding: 0px 5px;
    font-size: 12px;
    margin-left: 5px;
}
</style>