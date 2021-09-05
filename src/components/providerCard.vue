<template>
    <div>
        <div class="providerCard__block" v-bind:class="{ providerCard__block_short:  card_short > -1 && card_short < 4}">
            <div class="access_vendor" v-if="card_short > -1 && card_short < 4">Рекомендованный поставщик</div>
            <div class="providerCard">
                <div class="providerCard__image"></div>
                <div class="providerCard__information">
                    <div class="flex-title-star">
                        <h1>{{ name }}</h1>
                        <div class="stars">
                            <img src="../assets/images/star.svg">
                            <p class="stars__text">{{ rate_minpromtorg }}</p>
                        </div>
                    </div>
                    <h5>Адрес: {{ address }}</h5>
                    <h3>ИНН: {{ inn }}</h3>
                    <h3>КПП: {{ kpp }}</h3>
                    <h3>ОГРН: {{ ogrn }}</h3>
                    <h4><!--Наш бренд существует более 10 лет. У нас собственное производство, которое находится в городе Харьков (Украина), ассортимент нашего бренда достаточно разнообразный: мы производим платья, блузы, юбки, <span>подробнее</span>--></h4>
                    <div class="flex-phone-email">
                        <h3>{{ phone }}</h3>
                        <h3>{{ email }}</h3>
                        <h3>{{ website }}</h3>
                    </div>
                    <div class="down-section">
                        <svg v-on:click="addToFavorite(id)" v-bind:class="{ favorite: add_to_favorite == true }" width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M2.77216 3.77216C0.40928 6.13503 0.409282 9.96602 2.77216 12.3289L11.937 21.4937L12 21.4307L12.0631 21.4938L21.2279 12.329C23.5908 9.96609 23.5908 6.13511 21.2279 3.77223C18.865 1.40936 15.034 1.40936 12.6712 3.77224L12.3536 4.08978C12.1584 4.28505 11.8418 4.28505 11.6465 4.08978L11.3289 3.77216C8.96601 1.40928 5.13503 1.40928 2.77216 3.77216Z" stroke="#AFB1C3" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                        <div class="request-button" v-on:click="send_mail">
                            Разослать запрос
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
    import { bus } from '../main';
    import axios from 'axios';
    export default {
        props: ['id', 'address', 'email', 'inn', 'kpp', 'name', 'ogrn', 'phone', 'rate_minpromtorg', 'website', 'card_short'],
        data() {
            return {
                add_to_favorite: false
            }
        },
        methods: {
            send_mail() {
                axios.get('https://lagrange.creativityprojectcenter.ru/includes/api.php?module=send_vendor_mail&vendor_id=' + this.id)
                .then(response => {
                    console.log('id vendor')
                    console.log(this.id)
                    console.log('id vendor')
                    console.log(response)

                    if(response.data.status == false && response.data.reason == 'NO AUTH') {
                        bus.$emit('modalActive', {
                            modal_active: true,
                            modal_text: 'Чтобы рассылать запросы поставщикам, необходимо зарегистрироваться.'
                        })
                    } else if(response.data.status == false && response.data.reason == 'already sent today') {
                        bus.$emit('modalActive', {
                            modal_active: true,
                            modal_text: 'Вы уже отправили запрос данному поставщику.'
                        })
                    } else if(response.data.status == true) {
                        bus.$emit('modalActive', {
                            modal_active: true,
                            modal_text: 'Вы успешно отправили запрос этому поставщику. Следующий запрос можно будет отправить ему через 24 часа.'
                        })
                    }
                })
            },
            addToFavorite(idd) {
                this.add_to_favorite = true;
                axios
                .get('https://lagrange.creativityprojectcenter.ru/includes/api.php?module=add_to_favorites&vendor_id=' + idd)
                .then(response => {
                    console.log(response)
                })
            }
        }
    }
</script>
<style scoped lang="scss">
    .providerCard__block {
        border: 2px solid #D9DBE9;
        border-radius: 16px;
        display: inline-block;

        position: relative;
        .access_vendor {
            position: absolute;
            top: 3%;
            left: 3%;
            font-weight: 600;
            color: #8f6cc9;
        }
    }
    .providerCard__block_short {
        border: 2px solid #8f6cc9 !important;
    }
    .providerCard {
        display: flex;
        align-items: center;
        padding: 40px 40px;
        &__image {
            width: 240px;
            height: 240px;
            background-color: #E3DAF1;
            border-radius: 16px;
            margin-right: 46px;
        }
        &__information {
            max-width: 588px;
            color: #222222;
            h1 {
                font-weight: bold;
                font-size: 32px;
            }
            h2 {
                font-weight: 600;
                font-size: 14px;
            }
            h3 {
                font-weight: normal;
                font-size: 14px;
                margin-top: 4px;
            }
            h4 {
                font-weight: normal;
                font-size: 16px;
                margin-top: 2px;
                span {
                    color: #8f6cc9;
                    text-decoration: underline;
                }
            }
            h5 {
                font-weight: 600;
                font-size: 14px;
            }
            .flex-phone-email {
                display: flex;
                align-items: center;
                margin-top: 8px;
                h3 {
                    margin-right: 20px;
                }
            }
            .flex-title-star {
                display: flex;
                align-items: center;
                justify-content: space-between;
            }
            .stars {
                display: flex;
                img {
                    margin-right: 9px;
                }
                &__text {
                    font-weight: 600;
                    font-size: 16px;
                    color: #AFB1C3;
                }
            }
            .down-section {
                display: flex;
                align-items: center;
                float: right;
                margin-top: 14px;

                svg {
                    cursor: pointer;
                }

                svg.favorite path{
                    stroke: red;
                    fill: red;
                }
            }
            .request-button {
                cursor: pointer;
                font-weight: 600;
                font-size: 16px;
                color: white;
                padding: 4px 16px;
                background-color: #8F6CC9;
                border-radius: 40px;
                display: inline-block;
                margin-left: 18px;
                &:hover {
                    background-color: #9979ce;
                    transition: all 0.1s linear;
                }
            }
        }
    }
</style>