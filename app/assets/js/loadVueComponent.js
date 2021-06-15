import Vue from 'vue'
import Sample from './components/Sample.vue'
import Card from './components/Card.vue'

const app = new Vue({
  el: '#app',
  components: {
    Sample,
    Card
  },
})

// const card = new Vue({
//   template: '.card-component',
//   props: {
//     item: Object
//   },
//   components: {
//     Card
//   }
// })

export default {
  app
}
