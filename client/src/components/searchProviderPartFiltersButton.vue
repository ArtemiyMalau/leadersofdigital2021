<template>
    <div>
        <!--<div class="filters-button" v-on:click="press_filter_all" v-bind:class="{ filters_button__pressed: isPressedAll == true }">
            <div class="filters-button__flex">
                <p>Все</p>
                <img src="../assets/images/close-icon.svg" v-if="isPressedAll == true" >
            </div>
        </div>
        <div class="filters-button"  v-on:click="isPressedDillers=!isPressedDillers; checkPressedAll()" v-bind:class="{ filters_button__pressed: isPressedDillers == true }">
            <div class="filters-button__flex">
                <p>Дилеры</p>
                <img src="../assets/images/close-icon.svg" v-if="isPressedDillers == true">
            </div>
        </div>
        <div class="filters-button" v-on:click="isPressedManufactures=!isPressedManufactures; checkPressedAll()" v-bind:class="{ filters_button__pressed: isPressedManufactures == true }">
            <div class="filters-button__flex">
                <p>Производители</p>
                <img src="../assets/images/close-icon.svg" v-if="isPressedManufactures == true">
            </div>
        </div>
        <div class="filters-button" v-on:click="isPressedLogistics=!isPressedLogistics; checkPressedAll()" v-bind:class="{ filters_button__pressed: isPressedLogistics == true }">
            <div class="filters-button__flex">
                <p>Логистика</p>
                <img src="../assets/images/close-icon.svg" v-if="isPressedLogistics == true">
            </div>
        </div>-->
    </div>
</template>
<script>
    export default {
        data() {
            return {
                isPressedAll: false,
                isPressedDillers: false,
                isPressedManufactures: false,
                isPressedLogistics: false
            }
        },
        methods: {
            press_filter_all() {
                if(this.isPressedAll == true && this.isPressedDillers == true && this.isPressedManufactures == true && this.isPressedLogistics == true) {
                    this.isPressedAll = false;
                    this.isPressedDillers = false;
                    this.isPressedManufactures = false;
                    this.isPressedLogistics = false;
                } 
                else 
                {
                    this.isPressedAll = true;
                    this.isPressedDillers = true;
                    this.isPressedManufactures = true;
                    this.isPressedLogistics = true;
                }
            },
            checkPressedAll() {
                if(!(this.isPressedDillers && this.isPressedManufactures && this.isPressedLogistics)) {
                    this.isPressedAll = false;
                }
            }
        }
    }
</script>
<style scoped lang="scss">
    .filters-button {
        font-weight: 600;
        font-size: 16px;
        color: white;
        padding: 4px 16px;
        border: 1px solid #8F6CC9;
        border-radius: 40px;
        display: inline-block;
        color: #8F6CC9;
        cursor: pointer;
        margin-right: 8px;
    }
    .filters-button:last-child {
        margin-right: 0;
    }
    .filters-button:hover {
        background-color: #e3daf1;
        transition: all 0.1s linear;
    }
    .filters_button__pressed {
        background-color: #8F6CC9 !important;
        color: white !important;
    }
    .filters-button__flex {
        display: flex;
        img {
            margin-left: 10px;
        }
    }
</style>