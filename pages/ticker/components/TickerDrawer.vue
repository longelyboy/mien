<template>
  <van-popup v-model="show" position="right" :style="{ height: '100%' }">内容</van-popup>
</template>

<script>
import { mapState, mapActions } from 'vuex'
export default {
  data () {
    return {
      show: false
    }
  },
  computed: {
    ...mapState({
      tickerAll: ({ ticker }) => ticker.tickerAll
    })
  },
  mounted () {
    this.getTickerAll()
  },
  methods: {
    ...mapActions({
      getTickerAll: 'ticker/getTickerAll'
    })
  }
}
</script>

<style scoped lang="less">

</style>
