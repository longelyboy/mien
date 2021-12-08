<template>
  <transition :name="transitionName">
    <Nuxt />
  </transition>
</template>
<script>
import { mapState } from 'vuex'
export default {
  name: 'Default',
  transition: 'page',
  computed: {
    ...mapState({
      transitionName: ({ transitionName }) => transitionName
    })
  }
}
</script>
