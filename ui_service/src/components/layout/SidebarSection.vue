<template>
    <aside id="sidebar" class="sidebar">
        <ul class="sidebar-nav" id="sidebar-nav">
            <li class="nav-item">
                <a
                    class="nav-link"
                    :class="{ collapsed: !isActive('Chat') }"
                    href="#"
                    @click.prevent="triggerMenuClick('Chat')"
                >
                    <i class="bi bi-chat"></i>
                    <span>Chat</span>
                </a>
            </li>
            <li class="nav-item">
                <a
                    class="nav-link"
                    :class="{ collapsed: !isActive('Topic') }"
                    href="#"
                    @click.prevent="triggerMenuClick('Topic')"
                >
                    <i class="bi bi-book"></i>
                    <span>Knowledge</span>
                </a>
            </li>
            <li class="nav-item">
                <a
                    class="nav-link"
                    :class="{ collapsed: !isActive('Dataset') }"
                    href="#"
                    @click.prevent="triggerMenuClick('Dataset')"
                >
                    <i class="bi bi-file-earmark-text"></i>
                    <span>Dataset</span>
                </a>
            </li>
        </ul>
    </aside>
</template>

<script>
export default {
    name: "SidebarSection",
    emits: ["clickMenuButton"],
    data() {
        return {
            activeMenu: "Chat",
        };
    },
    methods: {
        triggerMenuClick(menu) {
            this.activeMenu = menu;
            this.$emit("clickMenuButton", menu);
        },
        isActive(menu) {
            return this.activeMenu == menu;
        },
    },
};
</script>

<style>
</style>