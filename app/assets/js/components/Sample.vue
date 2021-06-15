<template>
  <div>{{ msg }}</div>
</template>

<script>
export default {
  data () {
    return {
      msg: 'HELLO VUE VIA COMPONENT'
    }
  },
  mounted () {
    console.log('Called Component!!')
  }
}
</script>

<style>

</style>
