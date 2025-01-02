<template>
    <section
        class="section register min-vh-100 d-flex flex-column align-items-center justify-content-center py-4"
    >
        <div class="container">
            <div class="row justify-content-center">
                <div
                    class="col-lg-4 col-md-6 d-flex flex-column align-items-center justify-content-center"
                >
                    <div
                        class="d-flex justify-content-center py-4 align-middle"
                    >
                        <a
                            href="#"
                            class="logo d-flex align-items-center w-auto"
                        >
                            <img
                                src="@/assets/img/logo-full.png"
                                alt=""
                                width="100%"
                            />
                        </a>
                    </div>
                    <!-- End Logo -->

                    <div class="card mb-3">
                        <div class="card-body">
                            <div class="pt-4 pb-2">
                                <h5 class="card-title text-center pb-0 fs-4">
                                    Login to Your Account
                                </h5>
                            </div>

                            <form
                                class="row g-3 needs-validation"
                                novalidate=""
                                @submit.prevent="callLoginAPI"
                            >
                                <div class="col-12">
                                    <label for="yourUsername" class="form-label"
                                        >Username</label
                                    >
                                    <div class="input-group has-validation">
                                        <input
                                            type="text"
                                            name="username"
                                            class="form-control"
                                            id="yourUsername"
                                            required=""
                                            v-model="formData.username"
                                        />
                                        <div class="invalid-feedback">
                                            Please enter your username.
                                        </div>
                                    </div>
                                </div>

                                <div class="col-12">
                                    <label for="yourPassword" class="form-label"
                                        >Password</label
                                    >
                                    <input
                                        type="password"
                                        name="password"
                                        class="form-control"
                                        id="yourPassword"
                                        required=""
                                        v-model="formData.password"
                                    />
                                    <div class="invalid-feedback">
                                        Please enter your password!
                                    </div>
                                </div>

                                <div class="col-12">
                                    <div class="form-check">
                                        <input
                                            class="form-check-input"
                                            type="checkbox"
                                            name="remember"
                                            value="true"
                                            id="rememberMe"
                                        />
                                        <label
                                            class="form-check-label"
                                            for="rememberMe"
                                            >Remember me</label
                                        >
                                    </div>
                                </div>
                                <div class="col-12">
                                    <alert-box
                                        v-if="errorMsg.length > 0"
                                        :msg="errorMsg"
                                        @close="errorMsg = ''"
                                    />
                                </div>
                                <div class="col-12">
                                    <button
                                        class="btn btn-primary w-100"
                                        type="submit"
                                    >
                                        <span
                                            ><span
                                                v-if="showLoader"
                                                class="spinner-border spinner-border-sm"
                                                role="status"
                                                aria-hidden="true"
                                            ></span>
                                            Login</span
                                        >
                                    </button>
                                </div>
                                <div class="col-12">
                                    <p class="small mb-0">
                                        Don't have account?
                                        <a href="#">Create an account</a>
                                    </p>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>

<script>
import apiClient from "@/services/api/client";
import envVars from "@/services/env/vars"
import AlertBox from "@/components/ui/AlertBox.vue";

export default {
    name: "LoginView",
    components: { AlertBox },
    data() {
        return {
            formData: {
                username: "",
                password: "",
                grant_type: "password",
                client_id: envVars.VUE_APP_CLIENT_ID,
            },
            showLoader: false,
            errorMsg: "",
        };
    },
    methods: {
        showError(error) {
            this.errorMsg = error;
        },
        callLoginAPI() {
            this.showLoader = true;
            apiClient
                .post(
                    apiClient.urls.token,
                    new apiClient.typeCast.ToFormData(this.formData)
                )
                .then((response) => {
                    apiClient.setTokens(response.data);
                    this.callWhoamiAPI();
                })
                .catch((error) => {
                    if (error.isNetworkIssue()) {
                        this.showError("API Server not responding");
                    } else {
                        this.showError("Invalid username or password");
                    }
                })
                .finally(() => {
                    this.showLoader = false;
                });
        },
        callWhoamiAPI() {
            this.showLoader = true;
            apiClient
                .get(apiClient.urls.whoami)
                .then((response) => {
                    if (response.data.is_authenticated) {
                        this.$emit("onAuthenticate", response.data.user);
                    }
                })
                .catch((error) => {
                    if (error.isNetworkIssue()) {
                        this.showError("API Server not responding");
                    } else {
                        this.showError(
                            "Something went wrong while connecting API server"
                        );
                    }
                })
                .finally(() => {
                    this.showLoader = false;
                });
        },
    },
    created() {
        this.callWhoamiAPI();
    },
    emits: ["onAuthenticate"],
};
</script>

<style scoped>
</style>
