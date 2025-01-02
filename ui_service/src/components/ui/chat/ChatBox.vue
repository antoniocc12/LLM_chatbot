<template>
    <div class="pb-4" :class="[getParentClassName()]">
        <div>
            <img
                :src="getImageUrl()"
                class="rounded-circle mr-1"
                :alt="getUserType()"
                width="40"
                height="40"
            />
        </div>
        <div class="flex-shrink-1 bg-white rounded py-2 px-3 mx-3 response-container">
            <div class="fw-bold mb-1">
                {{
                    getUserType() === userType.JARVIS ? userType.JARVIS : "User"
                }}
            </div>
            <div v-if="isLoader()" class="dots ms-3"></div>
            <span v-else-if="isError()" class="text-danger">
                {{ msg.replace("./cmd.showError:", "") }}</span
            >
            <span v-else v-html="getHTMLMsg()" class="response-msg"></span>
            <p class="info" v-if="msgMeta">
                <span class="action-container">
                    <button
                        type="button"
                        class="btn"
                        :class="isCopied? 'btn-success': 'btn-light'"
                        :title="isCopied? 'Copied': 'Copy the content'"
                        @click.prevent="copy($event)">
                            <i class="bi bi-copy"></i>
                    </button>
                </span>
                <span v-if="msgMeta.source">Source: <b>{{msgMeta.source}}</b></span>
                <span v-if="msgMeta.page_no"> | Page: <b>{{msgMeta.page_no}}</b></span>
            </p>
        </div>
    </div>
</template>

<script>
import jarvisLogoUrl from "@/assets/img/logo.png";
import userLogoUrl from "@/assets/img/user.png";

export default {
    name: "ChatBox",
    props: ["msgFrom", "msg", "msgMeta"],
    data() {
        return {
            userType: {
                JARVIS: "JARVIS",
                USER: "USER",
            },
            isCopied: false,
            btnCopyTitle: "Copy the content"
        };
    },
    methods: {
        getHTMLMsg() {
            return this.msg.replaceAll("\n", "<br />");
        },
        getUserType() {
            if (this.msgFrom.toLowerCase() === "jarvis") {
                return this.userType.JARVIS;
            } else {
                return this.userType.USER;
            }
        },
        getImageUrl() {
            if (this.getUserType() === this.userType.JARVIS) {
                return jarvisLogoUrl;
            } else {
                return userLogoUrl;
            }
        },
        getParentClassName() {
            return {
                JARVIS: "chat-message-left",
                USER: "chat-message-right",
            }[this.getUserType()];
        },
        isLoader() {
            return (
                this.getUserType() === this.userType.JARVIS &&
                this.msg === "./cmd.showTyping"
            );
        },
        isError() {
            return (
                this.getUserType() === this.userType.JARVIS &&
                this.msg.startsWith("./cmd.showError:")
            );
        },
        copy(event) {
            let responseContainer = this.findParentByClassName(event.target, "response-container");
            if (responseContainer) {
                const messageContainer = responseContainer.querySelector('.response-msg');
                if (messageContainer) {
                    navigator.clipboard.writeText(messageContainer.innerText);
                    this.isCopied = true;
                    const self = this;
                    setTimeout(function(){ self.isCopied = false; }, 1000);
                }
            }
        },
        findParentByClassName(element, className) {
            while (element && element !== document) {
                if (element.classList.contains(className)) {
                    return element;
                }
                element = element.parentElement;
            }
            return null;
        }
    },
};
</script>

<style scoped>
.info {
    margin-bottom: 0;
    margin-top: 5px;
    font-size: 0.75rem;
    color: #999898;
    text-align: right;
}

.dots {
    width: 9.6px;
    height: 9.6px;
    background: #b0b1f6;
    color: #b0b1f6;
    border-radius: 50%;
    box-shadow: 16px 0, -16px 0;
    animation: dots-u8fzftsm 1s infinite linear alternate;
}

.action-container {
    float: left;
}

.action-container button {
    padding: 1px 5px;
    font-size: 12px;
    color: #999898;
}

.action-container button.btn-success {
    color: white;
}


@keyframes dots-u8fzftsm {
    0% {
        box-shadow: 16px 0, -16px 0;
        /* background: ; */
    }

    33% {
        box-shadow: 16px 0, -16px 0 rgba(176, 177, 246, 0.13);
        background: rgba(176, 177, 246, 0.13);
    }

    66% {
        box-shadow: 16px 0 rgba(176, 177, 246, 0.13), -16px 0;
        background: rgba(176, 177, 246, 0.13);
    }
}
</style>