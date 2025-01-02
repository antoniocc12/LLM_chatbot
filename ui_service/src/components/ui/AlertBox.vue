<template>
    <div
        class="alert alert-dismissible fade show" :class="alertClasses[type]"
        role="alert"
    >
        <i v-if="showIcon" class="bi" :class="iconClasses[type]"></i>

        <span>{{ msg }}</span>

        <button
            type="button"
            class="btn-close"
            aria-label="Close"
            @click="$emit('close')"
        ></button>
    </div>
</template>

<script>
export default {
    name: "AlertBox",
    emits: ["close"],
    props: {
        type: {
            type: String,
            default: "danger"
        },
        msg: {
            type: String,
            default: "Sample alert."
        }
    },
    data() {
        return {
            showIcon: true,
            alertClasses: {
                "info": "alert-info",
                "success": "alert-success",
                "warning": "alert-warning",
                "danger": "alert-danger",
            },
            iconClasses: {
                "primary": "bi-info-circle",
                "success": "bi-check-circle",
                "warning": "bi-exclamation-triangle",
                "danger": "bi-x-octagon",
            }
        }
    },
    methods: {
        getAlertClass() {


        }

    }
};
</script>

<style scoped>
i.bi {
    padding-right: 5px;
}
</style>