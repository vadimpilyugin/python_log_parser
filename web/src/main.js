import Vue from 'vue'
import App from './App.vue'

import Aggregation from './components/Aggregation.vue'
import MainPage from './components/MainPage.vue'


Vue.component('Aggregation', Aggregation)
Vue.component('MainPage', MainPage)

import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';

new Vue({
  el: '#app',
  render: h => h(App)
})
