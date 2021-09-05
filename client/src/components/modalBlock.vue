<template>
    <div>
        <div class="modal-window">
            <img src="../assets/images_identification/close-icon.svg" v-on:click="close_modal">
            <h1 class="modal_text" v-if="emailCorrected == true">Мы отправили вам письмо на почту <span>{{ emailClean }}</span>. Перейдите по ссылке, отправленной на вашу электронную почту, чтобы подтвердить аккаунт.</h1>
            <h1 class="modal_text" v-if="emailCorrected == false">Введенная почта {{ emailClean }} не существует, подтвердить аккаунт невозможно. Вы можете изменить почту в личном кабинете.</h1>
        </div>
    </div>
</template>
<script>
    export default {
        props: ['emailCorrected', 'emailClean'],
        data() {
            return {
                url: ''
            }
        },
        methods: {
            close_modal() {
                this.$emit('closeModalReg', false)
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