<template>
  <div class="w-full h-auto mx-auto relative shadow-sm bg-white rounded-lg">
  </div>
</template>

<script>
export default {
  props: {
    obj: {
      type: String
    }
  },
  data() {
    return {
      item: {}
    }
  },
  mounted() {
    this.item = JSON.parse(this.obj)
    console.log(this.obj)
    console.log(this.item)
  },
  methods: {
    getThumbnailImage() {
      if(this.item.image) {
        return this.item.image_thumbnail
      } else {
        return '/static/img/noimage.png'
      }
    }
  }
}
</script>

<style>

</style>
