<template>
  <div class="receive">
    <van-nav-bar
      :title="`${symbol}${$t('title')}`"
      left-arrow
      @click-left="$router.back()"
    />
    <div class="container">
      <van-tabs v-model="activeSymbol"
                class="tabs"
                type="card"
                @click="switchTab"
      >
        <van-tab
          title="TRC20"
          name="USDT-TRC"
        />
        <van-tab
          v-if="CHEKC_ERC"
          title="ERC20"
          name="USDT"
        />
      </van-tabs>
      <div class="qrcode-wrap">
        <qrcode-vue
          v-if="data.address"
          :value="data.address"
          size="180"
        ></qrcode-vue>
        <img
          v-else
          class="qrcode-default"
          src="@/assets/images/qrcode.svg"
        />
      </div>
      <div
        v-if="data.address"
        class="addr-wrap"
      >
        <span class="van-ellipsis_">{{ data.address }}</span>
        <van-button
          v-clipboard:copy="data.address"
          v-clipboard:success="onCopy"
          block
          type="info"
          class="addr-copy"
        >
          {{ $t('copy') }}
        </van-button>
      </div>
      <van-cell-group>
        <van-cell
          v-if="data.memo"
          :title="data.memo_name"
          :label="data.memo"
        />
        <van-cell
          :title="$t('tip')"
          :label="data.tips"
        />
      </van-cell-group>
    </div>
  </div>
</template>
<script>
import { mapState, mapActions } from 'vuex'
import QrcodeVue from 'qrcode.vue'
import { CHEKC_ERC } from '@/config/index'
export default {
  components: { QrcodeVue },
  i18n: {
    messages: {
      zh: {
        title: '收款地址',
        tip: '提示',
        copy: '复制'
      },
      en: { title: ' Receipt address', tip: 'Tips', copy: 'Copy' }
    }
  },
  data () {
    const symbol = this.$route.query.symbol
    return {
      symbol,
      CHEKC_ERC,
      data: {},
      activeSymbol: symbol
    }
  },
  computed: {
    ...mapState({
      currency: ({ currency }) => currency
    })
  },
  created () {
    this.loadData()
  },
  methods: {
    ...mapActions({
      walletAddr: 'wallet/walletAddr'
    }),
    loadData () {
      this.$toast.loading()
      const payload = {
        coin_symbol: this.activeSymbol,
        curency: this.currency.name
      }
      this.walletAddr(payload)
        .then(({ data }) => (this.data = data))
        .finally(() => {
          this.$toast.clear()
        })
    },
    onCopy () {
      this.$toast('复制成功')
    },
    switchTab (name) {
      this.loadData()
    }
  }
}
</script>
<style scoped lang="less">

.qrcode {
  &-wrap {
    margin-top: 36px;
    text-align: center;
    // border: 6px solid #dfeeff;
    width: 220px;
    height: 220px;
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 36px auto;
  }
  &-default {
    width: 200px;
    height: 200px;
  }
}
.addr {
  &-wrap {
    background-color: #fff;
    padding: 20px 10px;
  }
  &-copy {
    margin: 20px auto 0;
    width: 95%;
  }
}
.tips {
  &-wrap {
  }
}
.container {
  margin-top: 10px;
  background: #fff;
}
.tabs {
  .van-tabs__wrap{
   border-radius: 10px;
 }
}
.receive{
  background: #fff;
}
.receive  /deep/ .van-tabs__nav{
  border-radius: 14px;
  overflow: hidden;
}
.receive  /deep/ .van-tabs__nav  div:first-child{
   border-top-left-radius: 50px;
    border-bottom-left-radius: 50px;
}
.receive  /deep/ .van-tabs__nav  div:last-child{
    border-top-right-radius: 50px;
    border-bottom-right-radius: 50px;
}
.receive  /deep/ .van-tab--active{
  border: none;
}
.addr-wrap{
  overflow: hidden;
  .addr-copy{
    width: 90px;
    height: 50px;
    float: right;
    margin:0
  }
  .van-ellipsis_{
    width: calc(100% - 90px);
    display: block;
    float: left;
    height: 50px;
    line-height: 18px;
    word-wrap: break-word;
    background: #EFF2F6;
    padding: 6px 14px;
    box-sizing: border-box;
    font-weight: 700;
  }
}
.van-cell__title>span{

color: #EB4D5C;

}

</style>
