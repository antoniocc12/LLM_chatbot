<template>
    <header id="header" class="header fixed-top d-flex align-items-center">
        <div class="d-flex align-items-center justify-content-between">
            <a href="" class="logo d-flex align-items-center">
                <img src="@/assets/img/logo.png" alt="" />
                <span class="d-none d-lg-block">JARVIS</span>
            </a>
            <i
                v-if="!isAppModePlugin"
                class="bi bi-list toggle-sidebar-btn"
                @click="$emit('clickToggleSidebarButton')"
                title="Toggle Sidebar"
            ></i>
        </div>

        <nav class="header-nav ms-auto">
            <ul class="d-flex align-items-center">
                <li class="nav-item dropdown pe-3">
                    <a
                        class="nav-link nav-profile d-flex align-items-center pe-0"
                        href="#"
                        data-bs-toggle="dropdown"
                    >
                        <i class="bi bi-person-circle"></i>
                        <span class="d-none d-md-block dropdown-toggle ps-2">{{
                            getUsername(user)
                        }}</span> </a
                    ><!-- End Profile Iamge Icon -->

                    <ul
                        class="dropdown-menu dropdown-menu-end dropdown-menu-arrow profile"
                    >
                        <li class="dropdown-header">
                            <h6>{{ getUsername(user) }}</h6>
                            <span>{{ getUserType(user) }}</span>
                        </li>
                        <li>
                            <hr class="dropdown-divider" />
                        </li>

                        <!-- <li>
                            <a
                                class="dropdown-item d-flex align-items-center"
                                href="#"
                            >
                                <i class="bi bi-person"></i>
                                <span>My Profile</span>
                            </a>
                        </li>
                        <li>
                            <hr class="dropdown-divider" />
                        </li> -->

                        <!-- <li>
                            <a
                                class="dropdown-item d-flex align-items-center"
                                href="#"
                            >
                                <i class="bi bi-gear"></i>
                                <span>Account Settings</span>
                            </a>
                        </li>
                        <li>
                            <hr class="dropdown-divider" />
                        </li>

                        <li>
                            <a
                                class="dropdown-item d-flex align-items-center"
                                href="#"
                            >
                                <i class="bi bi-question-circle"></i>
                                <span>Need Help?</span>
                            </a>
                        </li>
                        <li>
                            <hr class="dropdown-divider" />
                        </li> -->

                        <li>
                            <a
                                class="dropdown-item d-flex align-items-center"
                                href="#"
                                @click.prevent="$emit('signOut')"
                            >
                                <i class="bi bi-box-arrow-right"></i>
                                <span>Sign Out</span>
                            </a>
                        </li>
                    </ul>
                    <!-- End Profile Dropdown Items -->
                </li>
                <!-- End Profile Nav -->
            </ul>
        </nav>
        <!-- End Icons Navigation -->
    </header>
</template>

<script>
import url from '@/services/utils/url.js';

export default {
    name: "HeaderSection",
    props: ["user"],
    emits: ["clickToggleSidebarButton", "signOut"],
    data() {
        return {
            isAppModePlugin: url.isAppModePlugin()
        };
    },
    methods: {
        getUsername(user) {
            let username = `${user.first_name} ${user.last_name}`;
            if (username.trim() == "") {
                username = user.username;
            }
            return username;
        },
        getUserType(user) {
            return user.is_superuser ? "Admin" : "User";
        },
    },
};
</script>

<style>
</style>