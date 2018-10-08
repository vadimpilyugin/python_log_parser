import Vue from 'vue'
import App from './App.vue'

import Aggregation from './components/Aggregation.vue'
import Counter from './components/Counter.vue'
import FileSelect from './components/FileSelect.vue'
import MainPage from './components/MainPage.vue'
import ErrorPopup from './components/ErrorPopup.vue'
// import PopupMessage from './components/PopupMessage.vue'
import Periodicity from './components/Periodicity.vue'
// import Blocks from './components/Blocks.vue'
// import TemplateEditor from './components/TemplateEditor.vue'


Vue.component('Aggregation', Aggregation)
Vue.component('Counter', Counter)
Vue.component('MainPage', MainPage)
Vue.component('FileSelect', FileSelect)
Vue.component('ErrorPopup', ErrorPopup)
// Vue.component('PopupMessage', PopupMessage)
Vue.component('Periodicity', Periodicity)
// Vue.component('Blocks', Blocks)
// Vue.component('TemplateEditor', TemplateEditor)

import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';

new Vue({
  el: '#app',
  render: h => h(App)
})
