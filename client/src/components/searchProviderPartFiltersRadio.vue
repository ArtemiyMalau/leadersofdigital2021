<template>
    <div>
        <div class="filtersRadio">
            <!--<input type="text" placeholder="Страна, Город" class="input-location">-->
            <citySearch/>
            <okvedsSearch/>
        </div>
    </div>
</template>
<script>
    import okvedsSearch from './okvedsSearch.vue';
    import citySearch from './citySearch.vue';
    export default {
        data() {
            return {
                volumeRadio: false,
                conditionsRadio: false,
                deliveryRadio: false,
                moneyRadio: false
            }
        },
        components: {
            okvedsSearch,
            citySearch
        }
    }
</script>
<style scoped lang="scss">
    * {
        color: #222222;
    }
    .filtersRadio {
        padding: 40px 40px;
        background: #FFFFFF;
        box-shadow: 0px 2px 18px rgba(143, 108, 201, 0.15);
        border-radius: 16px;
        display: inline-block;
    }
    input.input-location {
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
    }
    input::placeholder {
        font-weight: normal;
        font-size: 16px;
    }
    .radioFilters {
        &__flex {
            display: flex;
            padding-bottom: 8px;
            cursor: pointer;
        }
        &__block {
            margin-top: 16px;
            h1.radioFilters__title {
                font-weight: 600;
                font-size: 16px;
                margin-right: 6px;
            } 
            .radioFilter {
                label {
                    font-weight: normal;
                    font-size: 14px;
                }
            }  
        }
    }
    .custom-radio {
    position: absolute;
    z-index: -1;
    opacity: 0;
  }
  
    .custom-radio+label {
    display: inline-flex;
    align-items: center;
    user-select: none;
  }
  
    .custom-radio+label::before {
    content: '';
    display: inline-block;
    width: 1em;
    height: 1em;
    flex-shrink: 0;
    flex-grow: 0;
    border: 1px solid #adb5bd;
    border-radius: 50%;
    margin-right: 0.5em;
    background-repeat: no-repeat;
    background-position: center center;
    background-size: 50% 50%;
  }
  .custom-radio:not(:disabled):not(:checked)+label:hover::before {
    border-color: #8f6cc9;
    transition: all 0.1s linear;
  }
  .custom-radio:checked+label::before {
    border-color: #8F6CC9;
    background-color: #8F6CC9;
    background-image: url(../assets/images/check.svg);
  }
</style>