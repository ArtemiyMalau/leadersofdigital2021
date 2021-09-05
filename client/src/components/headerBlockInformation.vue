<template>
    <div>
        <div class="header__information">
            <div class="wrapper">
                <div class="text">
                    <h1>RosatomVendors</h1>
                    <p>Площадка для поиска поставщиков</p>
                </div>
                <div class="image">
                    <img src="../assets/images_header/main-image.svg">
                </div>
            </div>
        </div>
    </div>
</template>
<style lang="scss">
    .header {
        &__information {
            width: 100%;
            background-color: #F6F3FB;
            .wrapper {
                height: 284px;
                color: #222222;
                display: flex;
                align-items: center;
                justify-content: space-between;
                .image {
                    align-self: flex-end;
                    margin-bottom: -5px;
                    margin-right: -68px;
                }
                h1 {
                    font-weight: bold;
                    font-size: 64px;
                }
                p {
                    font-weight: normal;
                    font-size: 32px;
                }
            }
        }
    }
</style>