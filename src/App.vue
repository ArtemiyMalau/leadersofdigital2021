<template>
  <div id="app">
    <div class="background" v-bind:class="{ background_identification: show_registration == true || show_authorization == true || show_modal_active == true || show_modal_auth_active == true}">  
        <identificationBlock @emailCorrect="emailCorrectStatus" @showModal="show_modal" class="identification-block" @closeIdentificationForm="closeIdentificationFormAccept" v-if="show_registration == true || show_authorization == true" :showAuthorizationProps="show_authorization" :showRegistrationProps="show_registration"/>
        <modalBlock class="modal_block_style" v-if="show_modal_active == true" @closeModalReg="close_modal" :emailCorrected="email_correct_status" :emailClean="email_clean"/>
        <modalBlockAuth class="modal_block_style" v-if="show_modal_auth_active == true" :text="modal_auth_text" @closeModalStatusAuth="close_modal_auth"/>
    </div>   
    <div> 
        <headerBlock class="header-block" 
            @showRegistration="showRegistrationAccept" 
            @showAuthorization="showAuthorizationAccept"
            :authorizationStatusGlobal="authorization_status"
        ></headerBlock>
    </div>
  </div>
</template>

<script>
    import { bus } from './main';
    import axios from 'axios';
    import identificationBlock from './components/identificationBlock.vue';
    import headerBlock from './components/headerBlock.vue';
    import modalBlock from './components/modalBlock.vue';
    import modalBlockAuth from './components/modalBlockAuth.vue';
    //import searchProviderPart from './components/searchProviderPart.vue';
    //import headerBlockInformation from './components/headerBlockInformation.vue';
    export default {
        name: 'App',
        components: {
            //searchProviderPart,
            headerBlock,
            identificationBlock,
            modalBlock,
            modalBlockAuth
            //headerBlockInformation
        },
        data() {
            return {
                show_registration: false,
                show_authorization: false,
                authorization_status: '',
                show_modal_active: false,
                email_correct_status: '',
                email_clean: '',
                selectSearch: true,
                selectMessager: false,
                selectHuman: false,
                show_modal_auth_active: false,
                modal_auth_text: ''
            }
        },
        created() {
            axios
            .get('https://lagrange.creativityprojectcenter.ru/includes/api.php?module=check_auth')
            .then(response => {
                console.log('Статус авторизации после захода на страницу ')
                console.log(response)
                if(response.data.status == true) {
                    this.authorization_status = true;
                }
                if(response.data.status == false) {
                    this.authorization_status = false;
                }
            })
            bus.$on('checkAuthNow', data => {
                this.authorization_status = data;
                console.log('Статус авторизации сразу после регистрации ' + this.authorization_status)
            });
            bus.$on('checkedSearch', data => {
                this.authorization_status = data;
                console.log('Статус авторизации сразу после регистрации ' + this.authorization_status)
            });
            bus.$on('checkedMessager', data => {
                this.authorization_status = data;
                console.log('Статус авторизации сразу после регистрации ' + this.authorization_status)
            });
            bus.$on('checkedHuman', data => {
                this.authorization_status = data;
                console.log('Статус авторизации сразу после регистрации ' + this.authorization_status)
            });
            bus.$on('modalActive', data => {
                this.show_modal_auth_active = data.modal_active;
                this.modal_auth_text = data.modal_text;
            });
        },
        methods: {
            showRegistrationAccept(data) {
                this.show_registration = data.showRegistration;
                console.log(this.show_registration)
            },
            showAuthorizationAccept(data) {
                this.show_authorization = data.showAuthorization;
                console.log(this.show_authorization)
            },
            closeIdentificationFormAccept(data) {
                this.show_registration = data.statusIdentificationForm;
                this.show_authorization = data.statusIdentificationForm;
                console.log(this.show_registration)
            },
            show_modal(data) {
                this.show_modal_active = data.show_modal_status;
                console.log('статус модалки ' + this.show_modal_active)
            },
            close_modal(data) {
                this.show_modal_active = data;
                console.log('статус модалки ' + this.show_modal_active)
            },
            close_modal_auth(data) {
                this.show_modal_auth_active = data;
            },
            emailCorrectStatus(data) {
                this.email_correct_status = data.email_correct_status;
                this.email_clean = data.email_clean;
                console.log('пчота ' + this.email_correct_status)
                console.log('пчота ' + this.email_clean)
            }
        }
    }
</script>

<style>
    * {box-sizing: border-box;}
    a {text-decoration: none;}
    body, h1, h2, h3, h4, h5, h6, p {margin: 0; padding: 0;}
    * {font-family: 'Proxima Nova';}
    body {background-color: white;}
    .wrapper {max-width: 1280px;margin: 0 auto;}
    :active, :hover, :focus {outline: 0; outline-offset: 0;}

    .identification-block {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 11;
    }
    .background_identification:before {
        content: '';
        background: #14142B;
        position: fixed; 
        left: 0;
        top: 0;
        width: 100%; 
        height: 100%;
        opacity: 0.45;
        z-index: 10;
    }

    .modal_block_style {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 11 !important;
    }

    @font-face {
        font-family: 'Proxima Nova';
        src: url('./assets/fonts/ProximaNova-Bold.eot');
        src: local('Proxima Nova Bold'), local('ProximaNova-Bold'),
        url('./assets/fonts/ProximaNova-Bold.eot?#iefix') format('embedded-opentype'),
        url('./assets/fonts/ProximaNova-Bold.woff') format('woff'),
        url('./assets/fonts/ProximaNova-Bold.ttf') format('truetype');
        font-weight: bold;
        font-style: normal;
    }
    @font-face {
        font-family: 'Proxima Nova';
        src: url('./assets/fonts/ProximaNova-Regular.eot');
        src: local('Proxima Nova Regular'), local('ProximaNova-Regular'),
        url('./assets/fonts/ProximaNova-Regular.eot?#iefix') format('embedded-opentype'),
        url('./assets/fonts/ProximaNova-Regular.woff') format('woff'),
        url('./assets/fonts/ProximaNova-Regular.ttf') format('truetype');
        font-weight: normal;
        font-style: normal;
    }
    @font-face {
        font-family: 'Proxima Nova';
        src: url('./assets/fonts/ProximaNova-Semibold.eot');
        src: local('Proxima Nova Semibold'), local('ProximaNova-Semibold'),
        url('./assets/fonts/ProximaNova-Semibold.eot?#iefix') format('embedded-opentype'),
        url('./assets/fonts/ProximaNova-Semibold.woff') format('woff'),
        url('./assets/fonts/ProximaNova-Semibold.ttf') format('truetype');
        font-weight: 600;
        font-style: normal;
    }
</style>
