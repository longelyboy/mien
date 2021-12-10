<template>
  <div class="page">
    <transition :name="transitionName">
      <Nuxt />
    </transition>
    <nav-bar />
  </div>
</template>

<script>
import { mapState } from 'vuex'
import NavBar from '@/components/NavBar'
export default {
  name: 'Navigation',
  transition: 'page',
  components: { NavBar },
  computed: {
    ...mapState({
      transitionName: ({ transitionName }) => transitionName
    })
  }
}
</script>

<style lang="less" scoped>
.page {
  padding-bottom: 50px;
}
</style>
