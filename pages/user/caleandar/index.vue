<template>
  <div>
    <van-nav-bar :border="false" :title="$t('pageUser.history')" left-arrow @click-left="$router.back()" />
    <van-tabs v-model="active">
      <van-tab :title="$t('log')">
        <log></log>
      </van-tab>
      <van-tab :title="$t('order')"><order></order></van-tab>
    </van-tabs>
  </div>
</template>

<script>
import Log from './components/Log'
import Order from './components/Order'
export default {
  components: { Log, Order },
  i18n: {
    messages: {
      zh: {
        log: '交易日志',
        order: '交易订单'
      },
      en: {
        log: 'Transaction Log',
        order: 'Trade Orders'
      }
    }
  },
  data () {
    return {
      active: 0
    }
  }
}
</script>
<style lang="less" scoped>
</style>
