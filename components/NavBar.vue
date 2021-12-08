<template>
  <van-tabbar v-model="active" route z-index="100">
    <van-tabbar-item to="/home" icon="home-o">{{ $t('nav.home') }}</van-tabbar-item>
    <van-tabbar-item to="/market" icon="gold-coin-o">{{ $t('nav.exchange') }}</van-tabbar-item>
    <van-tabbar-item to="/ticker" icon="chart-trending-o">{{ $t('nav.ticker') }}</van-tabbar-item>
    <van-tabbar-item to="/user" icon="user-o">{{ $t('nav.user') }}</van-tabbar-item>
  </van-tabbar>
</template>

<script>
import { Tabbar, TabbarItem } from 'vant'
export default {
  components: {
    [Tabbar.name]: Tabbar,
    [TabbarItem.name]: TabbarItem
  },
  data () {
    return {
      active: 0
    }
  }
}
</script>

<style>
</style>
