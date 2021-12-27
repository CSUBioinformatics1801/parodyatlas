import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import VueRouter from 'vue-router'
import resault from './components/resault.vue'
import search from './components/search.vue'
import member from './components/member.vue'
import appcopy from './components/App copy.vue'

//import JsonViewer from 'vue-json-viewer'
//Vue.use(JsonViewer) 

Vue.use(VueRouter)

const routes = [
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ './views/About.vue')
  },
  {
    path:'/resault',
    name:'resault',
    component: resault
  },
  {
    path:'/member',
    name:'member',
    component:member
  },
  {
    path:'/',
    name:'search',
    component:search
  },
  {
    path:'/appcopy',
    name:'appcopy',
    component:appcopy
  }
]

const router = new VueRouter({
  routes
})

Vue.config.productionTip = false

new Vue({
  vuetify,
  router,
  render: h => h(App)
}).$mount('#app')
