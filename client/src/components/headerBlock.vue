<template>
    <div>
        <header class="header">
            <div class="header__main-part">
                <div class="wrapper">
                    <div class="header__logo">RosatomVendors</div>
                    <nav class="header__navigation" v-if="authorizationStatusGlobal == false">
                        <div class="header__search">
                            <img src="../assets/images_header/search-icon.svg">
                        </div>
                        <div class="header__identifications-buttons">
                            <div class="identification-button" v-on:click="showRegistrationEmit">Зарегистрироваться</div>
                            <div class="identification-button" v-on:click="showAuthorizationEmit">Войти</div>
                        </div>
                    </nav>
                    <nav class="header__navigation" v-if="authorizationStatusGlobal == true">
                        <div class="header__icon" v-on:click="checkedSearch = true; checkedMessager = false; checkedHuman = false; $router.push('/')" v-bind:class="{ header__icon_checked: checkedSearch == true }">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M11 20C15.9706 20 20 15.9706 20 11C20 6.02944 15.9706 2 11 2C6.02944 2 2 6.02944 2 11C2 15.9706 6.02944 20 11 20Z" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M22 22L18 18" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                        </div>
                        <div class="header__icon" v-on:click="checkedMessager = true; checkedHuman = false; checkedSearch = false;" v-bind:class="{ header__icon_checked: checkedMessager == true }">
                            <svg width="26" height="24" viewBox="0 0 26 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M7.00098 2C3.68727 2 1.00098 4.68629 1.00098 8V12C1.00098 12.2403 1.01511 12.4774 1.04259 12.7104C1.01489 12.802 1 12.8993 1 13V21.8258C1 22.6801 2.00212 23.141 2.65079 22.585L7.43827 18.4815C7.80075 18.1708 8.26243 18 8.73985 18H19.001C22.3147 18 25.001 15.3137 25.001 12V8C25.001 4.68629 22.3147 2 19.001 2H7.00098Z" stroke="white" stroke-width="2"/></svg>
                        </div>
                        <div class="header__icon" v-on:click="checkedHuman = true; checkedSearch = false; checkedMessager = false; $router.push('/personalArea')" v-bind:class="{ header__icon_checked: checkedHuman == true }">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 21.5L3.16547 20.4362C3.37405 19.0954 4.24842 17.9469 5.54504 17.5466C7.13654 17.0553 9.49052 16.5 12 16.5C14.5095 16.5 16.8635 17.0553 18.455 17.5466C19.7516 17.9469 20.6259 19.0954 20.8345 20.4362L21 21.5" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M12 12C14.7614 12 17 9.76142 17 7C17 4.23858 14.7614 2 12 2C9.23858 2 7 4.23858 7 7C7 9.76142 9.23858 12 12 12Z" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                        </div>
                    </nav>
                </div>
            </div>
        </header>
        <router-view></router-view>
    </div>
</template>
<script>
    import { bus } from '../main';
    export default {
        props: ['authorizationStatusGlobal'],
        data() {
            return {
                showRegistrationSend: false,
                showAuthorizationSend: false,
                checkedSearch: true,
                checkedMessager: false,
                checkedHuman: false
            }
        },
        methods: {
            showRegistrationEmit() {
                this.showRegistrationSend = !this.showRegistrationSend;
                this.$emit('showRegistration', {
                    showRegistration: this.showRegistrationSend
                })
            },
            showAuthorizationEmit() {
                this.showAuthorizationSend = !this.showAuthorizationSend;
                this.$emit('showAuthorization', {
                    showAuthorization: this.showAuthorizationSend
                })
            }
        },
        created() {
            bus.$on('closeIdentificationFormHeader', data => {
                console.log('closeident вызвался')
                this.showRegistrationSend = data;
                this.showAuthorizationSend = data;
            });
            bus.$on('checkHuman', data => {
                this.checkedHuman = data;
                this.checkedMessager = false;
                this.checkedSearch = false;
            });
        }
    }
</script>
<style scoped lang="scss">
    .header__icon:hover svg path{
        stroke: white;
        transition: all 0.1s linear;
    }
    .header__icon:hover {
        background-color: #b5a3d3;
        transition: all 0.1s linear;
        cursor: pointer;
    }
    .header__icon_checked {
        background-color: white !important;

        svg path {
            stroke: #8f6cc9 !important;
        }
    }

    .header__icon {
        padding: 17.1px 23px;
    }
    .header {
        &__logo {
            font-weight: 600;
            font-size: 18px;
            color: white;
            cursor: default;
        }
        &__main-part {
            width: 100%;
            background-color: #8F6CC9;
        }
        &__main-part .wrapper {
            height: 64px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        &__search {
            cursor: pointer;
        }
        &__identifications-buttons {
            display: flex;
            align-items: center;
            margin-left: 38px;
            .identification-button {
                font-weight: 600;
                font-size: 16px;
                color: white;
                padding: 4px 16px;
                border: 1px solid white;
                border-radius: 40px;
                display: inline-block;
                margin-left: 16px;
                cursor: pointer;
                &:first-child {
                    margin-left: 0;
                }
                &:hover {
                    background-color: white;
                    color: #8F6CC9;
                    transition: all 0.1s linear;
                }
            }
        }
        &__navigation {
            display: flex;
            align-items: center;
        }
    }
</style>
