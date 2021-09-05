<template>
    <div>
        <input class="okveds" type="text" v-model="searchText" @input="search" placeholder="ОКВЭД фильтр">
        <ul v-if="searchText !== ''" class="finded-cats">
            <li v-for="cat in findedCats" class="finded-cat" :key="cat.name">
                <div v-on:click="selectCategory(cat.name)">{{cat.name}}</div>
            </li>
        </ul>
    </div>
</template>
<script>
    import axios from 'axios';
    import { bus } from '../main';
    export default {
        data() {
            return {
                searchText: '',
                findedCats: [],
                categories: []
            }
        },
        methods: {
            findInCats(cat){
                console.log('findInCats выполнена')
                if(cat.name.toLowerCase().indexOf(this.searchText.toLowerCase()) !== -1){
                    this.findedCats.push(cat);
                }
            },
            search() {
                this.findedCats = [];
                if(this.searchText != '') {
                    for(let i = 0; i < this.categories.length; i++) {
                        this.findInCats(this.categories[i]);
                    }
                }
            },
            selectCategory(catSelected) {
                console.log(catSelected)
                bus.$emit('sendSelectOkved', catSelected);
            }
        },
        created() {
            axios.get('https://lagrange.creativityprojectcenter.ru/includes/api.php?module=get_okveds')
            .then(response => {
                this.categories = response.data.response.okveds;
                console.log(response)
                console.log(response.data.response.okveds[1070].name)
                console.log(this.categories.length)
            })
        }
    }
</script>
<style>
    input.okveds {
        -webkit-appearance: none;
        border: 0;
        width: 222px;
        height: 44px;
        border-radius: 16px;
        background: url(../assets/images/location-icon.svg) no-repeat 9% 50%, #FCFCFC;
        border: 1px solid #D9DBE9;
        font-weight: normal;
        font-size: 16px;
        color: black;
        padding: 0 20%;
        margin-top: 20px;
    }
    input::placeholder {
        font-weight: normal;
        font-size: 16px;
    }
    ul li {
        list-style: none;
        padding-bottom: 7px;
        font-size: 14px;
        cursor: pointer;
    }
    ul {
        padding: 0;
        width: 222px;
        margin: 0 auto;
        max-height: 500px;
        overflow-y: scroll;
    }
</style>