<template>
    <div :class="{ 'toggle-sidebar': isAppModePlugin ? true : !showSidebar }">
        <header-section
            @click-toggle-sidebar-button="showSidebar = !showSidebar"
            @sign-out="$emit('signOut')"
            :user="user"
        />

        <sidebar-section
            v-if="!isAppModePlugin"
            @click-menu-button="updateView"
        />

        <component :is="currentView" />

        <footer-section />
    </div>
</template>

<script>
import HeaderSection from "@/components/layout/HeaderSection.vue";
import SidebarSection from "@/components/layout/SidebarSection.vue";
import FooterSection from "@/components/layout/FooterSection.vue";

import ChatView from "./ChatView.vue";
import TopicView from "./TopicView.vue";
import DatasetView from "./DatasetView.vue";

import url from "@/services/utils/url.js";

const views = {
    ChatView: "ChatView",
    TopicView: "TopicView",
    DatasetView: "DatasetView",
};

const menuViewMapper = {
    Chat: "ChatView",
    Topic: "TopicView",
    Dataset: "DatasetView",
};

export default {
    name: "DashBoardView",
    props: ["user"],
    emits: ["signOut"],
    components: {
        HeaderSection,
        SidebarSection,
        FooterSection,
        ChatView,
        TopicView,
        DatasetView,
    },
    data() {
        return {
            showSidebar: true,
            currentView: views.ChatView,
            views: views,
            isAppModePlugin: url.isAppModePlugin(),
        };
    },
    methods: {
        updateView(menu) {
            this.currentView = menuViewMapper[menu];
        },
    },
};
</script>

<style>
</style>