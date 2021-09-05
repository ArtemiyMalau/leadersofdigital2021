import Vue from 'vue'
import App from './App.vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import VueTheMask from 'vue-the-mask'
import router from './router'
import vSelect from 'vue-select'

Vue.use(VueAxios, axios)
Vue.use(VueTheMask)

Vue.component('v-select', vSelect)
import 'vue-select/dist/vue-select.css';

Vue.config.productionTip = false

export const bus = new Vue();

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
