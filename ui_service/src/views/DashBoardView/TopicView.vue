<template>
    <main id="main" class="main">
        <div class="pagetitle">
            <h1><i class="bi bi-book"></i> Knowledge</h1>
            <nav>
                <ol class="breadcrumb">
                    <li class="breadcrumb-item">
                        <a href="">Home</a>
                    </li>
                    <li class="breadcrumb-item active">Knowledge</li>
                </ol>
            </nav>
            <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                <button
                    class="btn btn-sm btn-primary"
                    type="button"
                    data-bs-toggle="modal"
                    data-bs-target="#add-topic-modal"
                >
                    <i class="bi bi-plus-circle"></i> Add
                </button>
            </div>
        </div>
        <modal-add @on-topic-add="refreshDataTable" />
        <modal-edit :topic="selectedTopic" @on-topic-update="refreshDataTable" />
        <modal-delete :topic="selectedTopic" @on-topic-delete="refreshDataTable" />
        <data-table ref="topicDataTable" @on-action-btn-click="onDataTableActionBtnClick"/>
    </main>
</template>

<script>
import ModalAdd from "@/components/ui/topic/ModalAdd.vue";
import ModalEdit from "@/components/ui/topic/ModalEdit.vue";
import ModalDelete from "@/components/ui/topic/ModalDelete.vue";
import DataTable from "@/components/ui/topic/DataTable.vue";

export default {
    name: "TopicView",
    data() {
        return {
            selectedTopic: {
                id: "",
                name: "",
                slug: "",
                description: ""
            },
        };
    },
    components: {
        ModalAdd,
        ModalEdit,
        ModalDelete,
        DataTable,
    },
    methods: {
        refreshDataTable() {
            this.$refs.topicDataTable.callTopicListAPI();
        },
        onDataTableActionBtnClick(action, topic) {
            // action will be either 'edit' or 'delete'
            this.selectedTopic = topic;
        }
    }
};
</script>

<style>
</style>