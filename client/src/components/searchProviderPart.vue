<template>
    <div>
        <div class="wrapper">
            <div class="filters-flex">
                <div>
                    <div class="filter1-block">
                        <searchProviderPartInputSearch class="input__main-search" @maxPages="maxPagesAccept" @sendProviderInfo="accept_provide_info" :okved_filters="selectedOkvedFilters" :cities="selectedCities"></searchProviderPartInputSearch>
                        <div class="okved_filters_selected">
                            <h2 v-if="selectedOkvedFilters != ''">ОКВЭД фильтры:</h2>
                            <div class="okved_filter" v-for="item in selectedOkvedFilters" :key="item">
                                {{ item }} <span v-on:click="delete_filter_okved(selectedOkvedFilters.indexOf(item))"> (удалить)</span>
                            </div>
                        </div>
                        <div class="okved_filters_selected">
                            <h2 v-if="selectedCities != ''">Города:</h2>
                            <div class="okved_filter" v-for="item in selectedCities" :key="item">
                                {{ item }} <span v-on:click="delete_filter_city(selectedCities.indexOf(item))"> (удалить)</span>
                            </div>
                        </div>
                        <!--<div class="filter1-block__down-block">
                            <searchProviderPartFiltersButton class="input__filters-button"></searchProviderPartFiltersButton>
                            <div class="filter1-block__recomendation">
                                <p>Рекомендуемое</p>
                                <img src="../assets/images/down-icon.svg">
                            </div>
                        </div>-->
                    </div>
                    <div v-for="(card, i) in providerInfo" :key="i" style="padding-bottom: 20px;">
                        <providerCard
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
                            :card_short="i"
                            
                        />
                    </div>
                </div>
                <searchProviderPartFiltersRadio class="filter-radio"></searchProviderPartFiltersRadio>
            </div>
            <div class="paginationBlock">
                <div class="paginationBlock__arrow" v-on:click="pagination_left" v-if="page_number != 1">
                    <svg class="strelka-left-4" viewBox="0 0 100 85" height="22">
                    <polygon points="58.263,0.056 100,41.85 58.263,83.641 30.662,83.641 62.438,51.866 0,51.866 0,31.611 62.213,31.611 30.605,0 58.263,0.056" ></polygon>
                    </svg>
                </div>
                <p class="paginationBlock__page-number">{{ page_number }}</p>
                <div class="paginationBlock__arrow" v-on:click="pagination_right" v-if="page_number != max_pages">
                    <svg class="strelka-right-4" viewBox="0 0 100 85" height="22">
                    <polygon points="58.263,0.056 100,41.85 58.263,83.641 30.662,83.641 62.438,51.866 0,51.866 0,31.611 62.213,31.611 30.605,0 58.263,0.056" ></polygon>
                    </svg>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
    import { bus } from '../main';
    import searchProviderPartInputSearch from './searchProviderPartInputSearch.vue';
    //import searchProviderPartFiltersButton from './searchProviderPartFiltersButton.vue';
    import searchProviderPartFiltersRadio from './searchProviderPartFiltersRadio.vue';
    import providerCard from './providerCard.vue';
    export default {
        data() {
            return {
                selectedOkvedFilters: [],
                selectedCities: [],
                providerInfoAll: [],
                providerInfo: [],
                page_number: 1,
                max_pages: ''
            }
        },
        components: {
            searchProviderPartInputSearch,
            //searchProviderPartFiltersButton,
            searchProviderPartFiltersRadio,
            providerCard
        },
        created() {
            bus.$on('sendSelectOkved', data => {
                this.selectedOkvedFilters.push(data);
                console.log(this.selectedOkvedFilters)
            });
            bus.$on('sendSelectCities', data => {
                this.selectedCities.push(data);
                console.log(this.selectedCities)
            });
        },
        methods: {
            delete_filter_okved(id) {
                this.selectedOkvedFilters.splice(id, 1);
            },
            delete_filter_city(id) {
                this.selectedCities.splice(id, 1);
            },
            accept_provide_info(data) {
                this.providerInfoAll = data;
                console.log('пришло')
                console.log(this.providerInfoAll.provider_info.response.items)
                console.log('пришло')
                this.providerInfo = this.providerInfoAll.provider_info.response.items;
            },
            pagination_right() {
                this.page_number++;
                bus.$emit('pagination', this.page_number);
                console.log('pagination right')
            },
            pagination_left() {
                this.page_number--;
                bus.$emit('pagination', this.page_number);
                console.log('pagination left')
            },
            maxPagesAccept(data) {
                console.log('пришло макс')
                console.log(data)
                console.log('пришло макс')
                this.max_pages = data.max_pages;
            }
        }
    }
</script>
<style lang="scss">
    .strelka-left-4 {
        transform: rotate(180deg);
    }
    .paginationBlock {
        svg {
            cursor: pointer;
        }
        display: flex;
        align-items: center;
        padding-left: 450px;
        p.paginationBlock__page-number {
            cursor: default;
            font-size: 34px;
            padding: 0 20px;
        }
    }
    .okved_filters_selected {
        margin-top: 15px;
    }
    .okved_filter {
        cursor: default;
        span {
            cursor: pointer;
            color: #c8576a;
            text-decoration: underline;
        }
    }
    .filters-flex {
        display: flex;
        justify-content: space-between;
    }
    h2 {
        font-weight: 600;
        font-size: 23px;
        padding-bottom: 5px;
    }
    .filter1-block {
        padding: 32px 32px;
        background-color: white;
        display: inline-block;
        box-shadow: 0px 2px 18px rgba(143, 108, 201, 0.1);
        border-radius: 16px;
        margin-bottom: 40px;

        .filter1-block__down-block {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-top: 16px;
        }
        &__recomendation {
            cursor: pointer;
            display: flex;
            p {
                font-weight: 600;
                font-size: 16px;
                color: #8F6CC9;
            }
            img {
                vertical-align: middle;
                padding-left: 9px;
            }
        }
    }
</style>