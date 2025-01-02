<template>
    <footer id="footer" class="footer fixed-bottom">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <form @submit.prevent="onSubmit">
                    <div class="form-group mb-1">
                        <input
                            v-model="query"
                            type="text"
                            class="form-control form-control-lg"
                        />
                    </div>
                </form>
            </div>
        </div>
    </footer>
</template>

<script>
export default {
    name: "ChatBar",
    emits: ["onQuerySubmit"],
    data() {
        return {
            query: "",
        };
    },
    methods: {
        clearQuery() {
            this.query = "";
        },
        onSubmit() {
            const query = this.query.trim()
            if (query !== "") {
                this.$emit("onQuerySubmit", query);
                this.clearQuery();
            }
        },
    },
};
</script>

<style scoped>
.footer {
    background-color: white;
}
.footer input {
    background-color: #f6f9ff;
    border: solid 1px rgba(65, 84, 241, 0.6);
}
.fixed-bottom {
    z-index: 800;
    padding: 10px 10px;
}
</style>