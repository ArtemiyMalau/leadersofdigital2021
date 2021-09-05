<template>
    <div>
        <headerBlockInformation class="header-information-block" />
        <searchProviderPart class="search-provider-block"/>
    </div>
</template>
<script>
    import headerBlockInformation from './headerBlockInformation.vue';
    import searchProviderPart from './searchProviderPart.vue';
    export default {
        components: {
            headerBlockInformation,
            searchProviderPart
        }
    }
</script>
<style>
    .header-information-block {
        padding-bottom: 64px;
    }
    .search-provider-block {
        padding-bottom: 20px;
    }
</style>