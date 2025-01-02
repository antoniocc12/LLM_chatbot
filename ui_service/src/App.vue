<template>
    <login-view v-if="!isAuthenticated" @on-authenticate="authenticated" />
    <dash-board-view v-if="isAuthenticated" :user="user" @sign-out="signOut" />
</template>

<script>
import LoginView from "@/views/LoginView";
import DashBoardView from "@/views/DashBoardView";
import apiClient from "@/services/api/client";
import envVars from "@/services/env/vars";

export default {
    name: "App",
    components: {
        LoginView,
        DashBoardView,
    },
    data() {
        return {
            isAuthenticated: false,
            user: null,
        };
    },
    methods: {
        authenticated(user) {
            this.user = user;
            this.isAuthenticated = true;
        },
        signOut() {
            this.user = null;
            this.isAuthenticated = false;
            apiClient.clearTokens();
            apiClient.post(
                apiClient.urls.revokeToken,
                new apiClient.typeCast.ToFormData({
                    token: apiClient.accessToken,
                    client_id: envVars.VUE_APP_CLIENT_ID,
                })
            );
        },
    },
};
</script>

<style>
/* Theme */
.btn-primary {
    background-color: #4154f1;
}
.btn-primary:hover,
.btn-primary:active,
.btn-primary:first-child:active {
    background-color: #2a3def;
    border-color: #2a3def;
}

.form-group {
  margin-bottom: 1rem;
}
label {
  display: inline-block;
  margin-bottom: .5rem;
}
main#main {
    min-height: 510px;
}
</style>
