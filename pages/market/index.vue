<template>
  <div>
    <div safe-area-inset-top>
      <van-row
        type="flex"
        justify="space-between"
        align="center"
        class="page-header"
      >
        <!-- <van-col class="page-header-left">
          <h2 class="page-title">{{ $t('nav.exchange') }}</h2>
          <h2 class="page-title">{{ $t('nav.exchange') }}</h2>
        </van-col> -->
        <van-col class="tabs1" span="8" >
          <span ref="tabs1" @click="liFn(1)">{{ $t('nav.contract') }}</span>
        </van-col>
        <van-col class="tabs2" span="8">
          <span ref="tabs2" @click="liFn(2)">{{ $t('nav.spot')/* 现货*/ }}</span>
        </van-col>
      </van-row>
    </div>
    <van-tabs
      v-model="active"
      swipeable
      animated
      sticky
    >
      <van-tab
        v-for="item in platform"
        :key="item.name"
      >
        <template #title>{{ $t(item.label) }}</template>
        <template v-if="account">
          <div class="amount">{{ $t('balance') }} {{ Number(account['USDT'] ||account['BTC'] || 0) | numberFormat(8) }} USDT</div>
        </template>
        <template v-else>
          <div class="amount">
            <p>{{ $t('balance') }} {{ Number(account['USDT'] || 0) | numberFormat(8) }} USDT, {{ $t('not') }}</p>
            <nuxt-link to="/authorize">{{ $t('add') }}</nuxt-link>
          </div>
        </template>
        <assets-list ref="assetsList" v-if="typeShow==2" :platform="item.label"></assets-list> <!-- 现货 -->
        <assets-list-contract ref="assetsList1" v-else :platform="item.label"></assets-list-contract>
      </van-tab>
    </van-tabs>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import assetsList from './components/assetsList'
import assetsListContract from './components/assetsContract'
export default {
  layout: 'navigation',
  i18n: {
    messages: {
      zh: {
        not: '您还未添加该平台的API',
        add: '立即添加',
        balance: '账户余额'
      },
      en: {
        not: 'You have not added the platform\'s API',
        add: 'Add Now',
        balance: 'Balance'
      }
    }
  },
  components: {
    assetsList,
    assetsListContract
  },
  data () {
    return {
      active: 0,
      account: '',
      typeShow: 1,
    }
  },
  computed: {
    ...mapState({
      platform: ({ robot }) => robot.platform
    })
  },
  watch: {
    active (newVal) {

      if(this.typeShow == 1){
        this.account = ''
        this.apiAccountBalanceSwap({ platform: this.platform[newVal].label }).then((res) => {
          this.account = res.data.free
        })
      this.marketList1(this.typeShow,this.platform[newVal].label)
      }else{
        this.account = ''
        this.apiAccountBalance({ platform: this.platform[newVal].label }).then((res) => {
          this.account = res.data.free
        })
      this.marketList1(this.typeShow,this.platform[newVal].label)
      }
     
    },
    typeShow (newVal) {
      if(newVal == 1){
        this.account = ''
        this.apiAccountBalanceSwap({ platform: this.platform[this.active].label }).then((res) => {
          this.account = res.data.free
        })
      }else{
        this.account = ''
        this.apiAccountBalance({ platform: this.platform[this.active].label }).then((res) => {
          this.account = res.data.free
        })
      }
     
    }
  },
  mounted() {
    if(this.typeShow == 1){
        this.apiAccountBalanceSwap({ platform: this.platform[0].label }).then((res) => {
          this.account = res.data.free
        })
    }else{
      this.apiAccountBalance({ platform: this.platform[0].label }).then((res) => {
        this.account = res.data.free
      })
    }
    
  },
  methods: {
    ...mapActions({
      apiAccountBalance: 'authorize/apiAccountBalance',
      apiAccountBalanceSwap: 'authorize/apiSwapAccountBalance',
      marketList: 'robot/marketList',
      robotList: 'robot/robotList'
    }),
    liFn(type) {
      this.typeShow = type
      const platform = !this.active ? 'okex' : 'binance'
      this.marketList1(type,platform)
      if (type === 1) {
        this.$refs.tabs1.style.fontWeight = '700'
        this.$refs.tabs2.style.fontWeight = '400'
      } else {
        this.$refs.tabs1.style.fontWeight = '400'
        this.$refs.tabs2.style.fontWeight = '700'
      }
      this.$nextTick(() => {
       this.$refs[type == 2 ? 'assetsList' : 'assetsList1'][0].loadData();
      })
    },
    marketList1 (type,platform) {
       this.marketList({
        platform,
        type: type == 1 ? 'swap' : 'spot' // 合约
      })
    }
  },
  created(){
    this.marketList1(1,'okex')
  }
}
</script>

<style lang="less" scoped>
.tabs1,.tabs2{
color: #333333;
font-size: 18px;
line-height: 24px;
font-weight: 700;
text-align: right;
}
.tabs2{
  text-align: left;
  font-weight:400;
}
.page-header {
  background-color: #fff;
  height: 46px;
  padding: 0 15px;
  &-right .van-icon {
    display: inline-block;
    vertical-align: middle;
  }
  &-title {
    display: flex;
    align-items: center;
    font-size: 22px;
    line-height: 1;
    color: #333333;
  }
}
.amount {
  background-color: #F5F6F7;
  padding: 0 15px;
  height: 36px;
  font-size: 12px;
  display: flex;align-items: center;justify-content: space-between;
  a{
    color: #1678FF;
  }
}
.page-header-left{
  margin: auto;
}

</style>
