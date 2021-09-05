<template>
    <div>
        <div class="modal-window">
            <img src="../assets/images_identification/close-icon.svg" v-on:click="close_modal_auth">
            <h1 class="modal_text">{{ text }}</h1>
        </div>
    </div>
</template>
<script>
    export default {
        props: ['emailCorrected', 'emailClean', 'text'],
        data() {
            return {
                url: ''
            }
        },
        methods: {
            close_modal_auth() {
                this.$emit('closeModalStatusAuth', {
                    close_modal_auth: false
                })
            }
        }
    }
</script>
<style lang="scss">
    h1.modal_text {
        font-weight: 600;
        font-size: 22px;
        color: #222222;
        max-width: 500px;
        padding: 32px 32px;
        box-shadow: 0px 2px 18px rgba(143, 108, 201, 0.1);
        border-radius: 16px;
        background-color: white;
        text-align: center;

        span {
            color: #8f83d9;
        }
    }
    .modal-window {
        img {
            position: absolute;
            top: 10%;
            right: 5%;
            cursor: pointer;
        };
    }
</style>