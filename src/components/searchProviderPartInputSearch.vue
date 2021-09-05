<template>
    <div>
        <div class="input">
            <img src="../assets/images/search-icon.svg" v-on:click="main_search_button">
            <input type="text" class="search__input" placeholder="Поиск поставщиков" v-model="main_search">
        </div>
    </div>
</template>
<script>
    import { bus } from '../main';
    import axios from 'axios';
    export default {
        props: ['okved_filters', 'cities'],
        data() {
            return {
                main_search: ''
            }
        },
        methods: {
            main_search_button() {
                console.log('фильтры')
                console.log(this.okved_filters)
                axios.post('https://lagrange.creativityprojectcenter.ru/includes/api.php', {
                    module: 'okved_search',
                    okveds_names: this.okved_filters,
                    cities: this.cities,
                    query: this.main_search,
                    page: 1
                })
                .then(response => {
                    console.log('отправилось')
                    console.log(response)
                    console.log('отправилось')
                    this.$emit('sendProviderInfo', {
                        provider_info: response.data
                    });
                    this.$emit('maxPages', {
                        max_pages: response.data.response.count_page
                    })
                })
            }
        },
        created() {
            axios.post('https://lagrange.creativityprojectcenter.ru/includes/api.php', {
                    module: 'okved_search',
                    okveds_names: [],
                    cities: [],
                    query: '',
                    page: 1
                })
                .then(response => {
                    console.log('отправилось')
                    console.log(response.data.response.count_page)
                    this.$emit('maxPages', {
                        max_pages: response.data.response.count_page
                    })
                    console.log('отправилось')
                    this.$emit('sendProviderInfo', {
                        provider_info: response.data
                    });
                })
            bus.$on('pagination', data => {
                axios.post('https://lagrange.creativityprojectcenter.ru/includes/api.php', {
                    module: 'okved_search',
                    okveds_names: this.okved_filters,
                    cities: this.cities,
                    query: this.main_search,
                    page: data
                })
                .then(response => {
                    this.$emit('sendProviderInfo', {
                        provider_info: response.data
                    });
                })
            });
        }
    }
</script>
<style lang="scss">
    .input {
        position: relative;
        img {
            position: absolute;
            top: 33%;
            right: 3%;
            cursor: pointer;
        }
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
    }
    input::placeholder {
        font-weight: normal;
        font-size: 16px;
    }
</style>