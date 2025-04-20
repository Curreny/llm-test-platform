/*
=========================================================
Muse - Vue Ant Design Dashboard - v1.0.0
=========================================================

Product Page: https://www.creative-tim.com/product/vue-ant-design-dashboard
Copyright 2021 Creative Tim (https://www.creative-tim.com)
Coded by Creative Tim

=========================================================
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software. 
*/

import Vue from 'vue'
import Antd from 'ant-design-vue';
import 'ant-design-vue/dist/antd.css';
import App from './App.vue'
import DefaultLayout from './layouts/Default.vue'
import DashboardLayout from './layouts/Dashboard.vue'
import DashboardRTLLayout from './layouts/DashboardRTL.vue'
import SimpleLayout from './layouts/SimpleLayout.vue'
import router from './router'
// import './plugins/click-away'

// 引入ECharts
import * as echarts from 'echarts'

// 引入highlight.js用于代码高亮
import VueHighlightJS from 'vue-highlightjs'
import 'highlight.js/styles/github.css'

import './scss/app.scss';

Vue.use(Antd);
// 使用highlight.js
Vue.use(VueHighlightJS);

// 将ECharts挂载到Vue原型上，方便组件内使用
Vue.prototype.$echarts = echarts

Vue.config.productionTip = false

// Adding template layouts to the vue components.
Vue.component("layout-default", DefaultLayout);
Vue.component("layout-dashboard", DashboardLayout);
Vue.component("layout-dashboard-rtl", DashboardRTLLayout);
Vue.component("layout-simple", SimpleLayout);

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')