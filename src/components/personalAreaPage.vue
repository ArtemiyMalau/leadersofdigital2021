<template>
    <div>
        <div class="personalArea">
            <div class="wrapper">
                <div class="personalArea__menu">
                    <div class="personalArea__image"></div>
                    <div class="personalArea__client-name">
                        <h1>{{ first_name }}</h1> 
                        <h1>{{ last_name }}</h1>
                    </div>
                    <div class="personalArea__client-status">
                        <div class="client-status__text">
                            <p v-if="local_user_type == 1">Покупатель</p>
                            <p v-if="local_user_type == 2">Поставщик</p>
                        </div>
                        <div class="client-status__image">
                            <img src="../assets/images_personalarea/alert_info.svg">
                        </div>
                    </div>
                    <nav class="personalArea__navigation">
                        <div class="nav__link" v-on:click="star_part" v-bind:class="{ nav__link__active: star_part_status == true }">Избранное</div>
                        <div class="nav__link" v-on:click="history_part" v-bind:class="{ nav__link__active: history_part_status == true }">История запросов</div>
                        <div class="nav__link" v-on:click="manage_part" v-bind:class="{ nav__link__active: manage_part_status == true }">Настройки</div>
                    </nav>
                </div>
                <div class="personalArea__manage" v-if="manage_part_status == true">
                    <h1 class="personalArea__title">Личный кабинет</h1>
                    <h2 class="personalArea__suptitle">Изменить данные</h2>
                    <h6 class="alert__window" v-if="alert_message != ''">{{ alert_message }}</h6>
                    <div class="personalArea__inputs-flex">
                        <div class="personalArea__inputs">
                            <div class="personalArea__input">
                                <p class="input-title">Имя</p>
                                <input type="text" placeholder="Анастасия" v-model="name_change">
                            </div>
                            <div class="personalArea__input">
                                <p class="input-title">Фамилия</p>
                                <input type="text" placeholder="Скоморохова" v-model="lastname_change">
                            </div>
                        </div>
                        <div class="personalArea__inputs">
                            <div class="personalArea__input">
                                <p class="input-title">Почта</p>
                                <input type="text" placeholder="mail@gmail.com" v-model="email_change">
                            </div>
                            <div class="personalArea__input">
                                <p class="input-title">Номер телефона</p>
                                <input type="text" placeholder="+7 (900) 990-90-90" v-model="phone_change">
                            </div>
                        </div>
                    </div>
                    <h2 class="personalArea__suptitle">Сменить пароль</h2>
                    <div class="personalArea__inputs-blocks">
                        <div class="personalArea__input">
                            <p class="input-title">Старый пароль</p>
                            <input type="text" placeholder="***********" v-model="old_password">
                        </div>
                        <div class="personalArea__input">
                            <p class="input-title">Новый пароль</p>
                            <input type="text" placeholder="***********" v-model="new_password">
                        </div>
                        <div class="personalArea__input">
                            <p class="input-title">Повторите новый пароль</p>
                            <input type="text" placeholder="***********" v-model="accept_new_password">
                        </div>
                    </div>
                    <div class="saveManageButton" v-on:click="change_button">Сохранить последние изменения</div>
                </div>
                <div class="personalArea__history" v-if="history_part_status == true">
                    <h1 class="personalArea__title">Личный кабинет</h1>
                    <div class="history__input">
                        <img src="../assets/images/search-icon.svg">
                        <input type="text" placeholder="Поиск сделок">
                    </div>
                    <div class="history__table">
                        <div class="history__table-header">
                            <div style="width: 75px; text-align: center;"><p>№</p></div>
                            <div style="width: 165px; text-align: center;"><p>Почта</p></div>
                            <div style="width: 365px; text-align: center;"><p>Наименование сделки</p></div>
                            <div style="width: 160px; text-align: center;"><p>ИНН</p></div>
                            <div style="width: 120px; text-align: center;"><p>Оценка</p></div>
                        </div>
                        <div class="history__table-body">
                            <div class="history__table-item" v-for="(item, i) in getMailesSend" :key="i">
                                <div style="width: 75px;"><p style="font-size: 14px; text-align: center;">{{ i+1 }}</p></div>
                                <div style="width: 165px;"><p style="font-size: 14px; text-align: center;">{{ item.email }}</p></div>
                                <div style="width: 365px;"><p style="font-size: 14px; text-align: center;">{{ item.name }}</p></div>
                                <div style="width: 160px;"><p style="font-size: 14px; text-align: center;">{{ item.inn }}</p></div>
                                <div style="width: 120px;"><p style="font-size: 14px; text-align: center;">{{ item.rate_minpromtorg }}</p></div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="personalArea__favorites" v-if="star_part_status == true">
                     <h1 class="personalArea__title">Личный кабинет</h1>
                    <div class="history__input">
                        <img src="../assets/images/search-icon.svg">
                        <input type="text" placeholder="Поиск поставщиков">
                    </div>
                    <div v-for="(card, i) in getAllFavorites" :key="i" style="padding-bottom: 20px;">
                        <providerCard style=""
                            :address="card.address" 
                            :email="card.email"
                            :inn="card.inn"
                            :kpp="card.kpp"
                            :name="card.name"
                            :ogrn="card.ogrn"
                            :phone="card.phone"
                            :rate_minpromtorg="card.rate_minpromtorg"
                            :website="card.website"
                            :id="card.id"
                        />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
    import { bus } from '../main';
    import providerCard from './providerCard.vue';
    import axios from 'axios';
    export default {
        data() {
            return {
                star_part_status: false,
                history_part_status: false,
                manage_part_status: true,
                name_change: '',
                lastname_change: '',
                email_change: '',
                phone_change: '',
                old_password: '',
                new_password: '',
                accept_new_password: '',
                alert_message: '',
                local_user_type: '',
                first_name: '',
                last_name: '',
                getMailesSend: [],
                getAllFavorites: []
            }
        },
        components: {
            providerCard
        },
        methods: {
            star_part() {
                this.star_part_status = true,
                this.history_part_status = false,
                this.manage_part_status = false
            },
            history_part() {
                this.star_part_status = false,
                this.history_part_status = true,
                this.manage_part_status = false
            },
            manage_part() {
                this.star_part_status = false,
                this.history_part_status = false,
                this.manage_part_status = true
            },
            change_button() {
                console.log(this.name_change)
                axios
                .post('https://lagrange.creativityprojectcenter.ru/includes/api.php', {
                    module: 'change_user_data',
                    user_type: this.local_user_type,
                    email: this.email_change,
                    phone: this.phone_change,
                    old_password: this.old_password,
                    new_password: this.new_password,
                    name: this.name_change,
                    optional_name: this.lastname_change
                })
                .then(response => {
                    console.log(response)
                    axios
                    .get('https://lagrange.creativityprojectcenter.ru/includes/api.php?module=get_user_data')
                    .then(response => {
                        console.log(response)
                        this.first_name = response.data.response.first_name;
                        this.last_name = response.data.response.last_name;
                    })
                })
            }
        },
        created() {
            bus.$emit('checkHuman', true);
            axios
            .get('https://lagrange.creativityprojectcenter.ru/includes/api.php?module=get_user_data')
            .then(response => {
                console.log(response)
                console.log('user data')
                console.log(response)
                this.first_name = response.data.response.first_name;
                this.last_name = response.data.response.last_name;
                this.local_user_type = response.data.response.user_type;
            })
            axios
            .get('https://lagrange.creativityprojectcenter.ru/includes/api.php?module=get_mailes_send')
            .then(response => {
                console.log(response)
                this.getMailesSend = response.data.items;
            })
            axios
            .get('https://lagrange.creativityprojectcenter.ru/includes/api.php?module=get_all_favorites')
            .then(response => {
                this.getAllFavorites = response.data.items;
                console.log(this.getAllFavorites)
            })
        }
    }
</script>
<style lang="scss">
    .personalArea {
        .wrapper {
            display: flex;
        }
        &__favorites {
            margin-top: 64px;
            margin-left: 38px;
            h1.personalArea__title {
                font-weight: bold;
                font-size: 32px;
                padding-bottom: 20px;
            }
            .history__input {
                position: relative;
                padding-bottom: 24px;
                img {
                    position: absolute;
                    cursor: pointer;
                    top: 24%;
                    right: 3%;
                }
                input {
                    -webkit-appearance: none;
                    border: 0;
                    width: 955px;
                    height: 64px;
                    border-radius: 16px;
                    padding: 0 2%;
                    background: #EFF0F6;
                    font-weight: normal;
                    font-size: 16px;
                    color: black;
                    &::placeholder {
                        font-weight: normal;
                        font-size: 16px;
                        color: #AFB1C3;
                    }
                }
            }
        }
        &__history {
            margin-top: 64px;
            margin-left: 38px;
            h1.personalArea__title {
                font-weight: bold;
                font-size: 32px;
                padding-bottom: 20px;
            }
            .history__input {
                position: relative;
                padding-bottom: 24px;
                img {
                    position: absolute;
                    cursor: pointer;
                    top: 24%;
                    right: 3%;
                }
                input {
                    -webkit-appearance: none;
                    border: 0;
                    width: 890px;
                    height: 64px;
                    border-radius: 16px;
                    padding: 0 2%;
                    background: #EFF0F6;
                    font-weight: normal;
                    font-size: 16px;
                    color: black;
                    &::placeholder {
                        font-weight: normal;
                        font-size: 16px;
                        color: #AFB1C3;
                    }
                }
            }
            .history__table {
                font-weight: 600;
                font-size: 18px;
                color: #6E7191;
            }
            .history__table-header {
                display: flex;
                align-items: center;
                padding-bottom: 10px;
            }
            .history__table-item {
                display: flex;
                margin-bottom: 5px;
                border: 2px solid #D9DBE9;
                border-radius: 16px;
                margin-bottom: 5px;
            }
        }
        &__manage {
            width: 628px;
            margin-top: 64px;
            margin-left: 38px;
            input {

                font-weight: normal;
                font-size: 16px;
                color: black;

                z-index: 1;
                -webkit-appearance: none;
                border: 0;
                width: 302px;
                height: 63px;
                border: 2px solid #D9DBE9;
                border-radius: 16px;
                padding-left: 22px;
                padding-right: 64px;
                padding-top: 28px;
                background-color: #FCFCFC;
            }
            .personalArea__inputs-flex {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding-bottom: 10px;
            }
            .saveManageButton {
                padding: 8px 24px;
                background-color: #8F6CC9;
                border-radius: 21px;
                font-weight: 600;
                font-size: 18px;
                color: white;
                display: inline-block;
                float: right;
                margin-top: 30px;
                cursor: pointer;
            }
            .personalArea__input {
                margin-bottom: 16px;
                //margin-right: 24px;
                position: relative;
                z-index: 1;

                p.input-title {
                    position: absolute;
                    left: 23px;
                    top: 7px;
                    z-index: 20;

                    font-weight: 600;
                    font-size: 14px;
                    color: #6E7191;

                }
            }
            input::placeholder {
                font-weight: normal;
                font-size: 16px;
                color: #AFB1C3;
            }
            h1.personalArea__title {
            font-weight: bold;
            font-size: 32px;
            color: #222222;
            }
            h2.personalArea__suptitle {
                font-weight: 600;
                font-size: 24px;
                color: #222222;
                margin-top: 5px;
                padding-bottom: 16px;
            }
            h6.alert__window {
                font-weight: normal;
                font-size: 16px;
                color: white;
                background-color: #b84250;
                display: inline-block;
                margin-bottom: 15px;
            }
        }
        &__menu {
            width: 288px;
            height: 100%;
            display: block;
            background: #F6F3FB;
            padding: 54px 0;
        }
        &__image {
            width: 128px;
            height: 128px;
            background: #C4C4C4;
            border-radius: 50%;
            margin: 0 auto;
            
        }
        &__client-name {
            margin-top: 27px;
            h1 {
                font-weight: bold;
                font-size: 32px;
                color: #6E7191;
                text-align: center;
                line-height: 0.95;
            }
        }
        &__client-status {
            display: flex;
            justify-content: center;
            margin-top: 16px;
            .client-status__text {
                p {
                    font-weight: 600;
                    font-size: 16px;
                    color: white;
                    padding: 4px 16px;
                    background-color: #8F6CC9;
                    border-radius: 40px;
                    display: inline-block;
                }
            }
            .client-status__image {
                margin-left: 9px;
                img {
                    margin-top: 2px;
                }
            }
        }
        &__navigation {
            padding-bottom: 150px;
            margin-top: 56px;
            .nav__link {
                font-weight: 60;
                font-size: 24px;
                color: rgba(110, 113, 145, 0.5);
                margin-left: 54px;
                padding-bottom: 16px;
                cursor: pointer;
            }
            .nav__link__active {
                color:#6E7191 !important;
            }
            .nav__link:hover {
                color: #7b7d93;
                transition: all 0.1s linear;
            }
        }
    }
</style>