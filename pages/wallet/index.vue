<template>
  <div class="wellet">
    <van-nav-bar
      :title="`${$t('title')}`"
      left-arrow
      style="
      color:#fff;"
      @click-left="$router.back()"
    />
    <div class="detail-info">
      <ul >
        <li :class="tab === 1?'tab':''" @click="switch_(1)">{{ $t('usdt') }}</li>
        <li :class="tab === 2?'tab':''" @click="switch_(2)">{{ $t('integral') }}</li>
      </ul>
      <van-row v-if="tab === 1">
        <van-col span="20">
          <div class="detail-title">{{ $t('total') }}（{{ symbol }}）</div>
          <div class="detail-amount">{{ detailInfo.cloud_balance | numberFormat(8) }}</div>
          <!-- <div class="detail-price">≈{{ currency.symbol }} {{ detailInfo.price }}</div> -->
        </van-col>
        <van-col span="4">
          <!-- <van-icon
            :name="detailInfo.img_url"
            size="54"
          /> -->
        </van-col>
      </van-row>
      <van-row v-else-if="tab === 2">
        <van-col span="20">
          <div class="detail-amount">{{ userInfo.balance| numberFormat(8) }}</div>
        </van-col>
      </van-row>
      <!-- <div class="copy-wrap">
            <span class="van-ellipsis">{{ detailInfo.address ? detailInfo.address : '^-^' }}</span>
            <van-button
              v-if="detailInfo.address"
              v-clipboard:copy="detailInfo.address"
              v-clipboard:success="onCopy"
              plain
              type="info"
              size="mini"
            >复 制</van-button>
          </div> -->
      <div class="btn-group">
        <ul v-if="tab === 1">
          <li>
            <img src="../../assets/images/cz.png" alt="">
            <p @click="handleLink('/wallet/receive')"> {{ $t('receipt') }}</p>
          </li>
          <li>
            <img src="../../assets/images/tx.png" alt="">

            <p @click="handleLink('/wallet/withdraw')"> {{ $t('withdraw') }}</p>
          </li>
        </ul>
        <ul v-if="INTEGR_ALDRAW && tab ===2">
          <li style="width: 100%;">
            <img src="../../assets/images/jfcj.png" alt="">
            <p @click="handleLink('/user/game')"> {{ $t('Integraldraw') }}</p>
          </li>
        </ul>
      </div>
    </div>

    <div v-if="tab === 1" class="bill-list">
      <div class="bill-title">{{ symbol }} {{ $t('bill') }}</div>
      <van-pull-refresh
        v-model="refreshing"
        class="pull-refresh"
        @refresh="onRefresh"
      >
        <van-list
          v-model="loading"
          :finished="finished"
          :finished-text="$t('finished_text')"
          @load="onLoad"
        >
          <van-cell
            v-for="item in list"
            :key="item.id"
            center
            :title="`${Number(item.amount).toFixed(5) > 0 ? '+'+Number(item.amount).toFixed(5) : Number(item.amount).toFixed(5)}`"
            :value="item.type_msg"
            :label="timeFormat(item.log_time)"
          />
        </van-list>
      </van-pull-refresh>
    </div>
    <div v-else-if="tab === 2" class="bill-list">
      <div class="bill-title"> {{ $t('Integralbills') }}</div>
      <van-pull-refresh
        v-model="refreshing"
        class="pull-refresh"
        @refresh="onRefresh"
      >
        <van-list
          v-model="loading"
          :finished="finished"
          :finished-text="$t('finished_text')"
          @load="onLoad"
        >
          <van-cell
            v-for="item in list2"
            :key="item.id"
            center
            :title="`${Number(item.change).toFixed(5) > 0 ? '+'+Number(item.change).toFixed(5) : Number(item.change).toFixed(5)}`"
            :value="item.extension"
            :label="timeFormat(item.ctime)"
          />
        </van-list>
      </van-pull-refresh>
    </div>
  </div>
</template>
<script>
import { Swipe, SwipeItem } from 'vant'
import { mapState, mapActions } from 'vuex'
import { format as timeFormat } from '@/utils/time'
import { INTEGR_ALDRAW } from '@/config/index'

export default {
  i18n: {
    messages: {
      zh: {
        title: '我的资产',
        total: '总资产折合',
        receipt: '充值',
        withdraw: '提币',
        usdt: 'USDT资产',
        integral: '积分资产',
        Integraldraw: '积分抽奖',
        Integralbills: '积分账单'
      },
      en: {
        title: 'My Assets',
        total: 'Total Assets',
        receipt: 'Receipt',
        withdraw: 'withdraw',
        usdt: 'USDT Assets',
        integral: 'Integral Assets',
        Integralbills: 'Integral Bills'
      }
    }
  },
  components: {
    [Swipe.name]: Swipe,
    [SwipeItem.name]: SwipeItem
  },
  data () {
    return {
      INTEGR_ALDRAW,
      tab: 1,
      symbol: this.$route.query.symbol,
      width: window.innerWidth - 30,
      detailInfo: {},
      list: [],
      loading: false,
      finished: false,
      refreshing: false,
      offset: 0,
      limit: 20,
      list2: [],
      loading2: false,
      finished2: false,
      refreshing2: false,
      offset2: 0,
      limit2: 20,
      activeIndex: 0
    }
  },
  computed: {
    ...mapState({
      currency: ({ currency }) => currency,
      userInfo: ({ user }) => user.userInfo
    })
  },
  created () {
    this.loadFundList()
    this.loadDetail()
    this.getintegralList()
  },
  methods: {
    getintegralList () {
      this.integralList({})
        .then(({ data }) => {
          this.list2 = data.list
        })
    },
    switch_(type) {
      this.tab = type
      if (type === 1) {
        this.loadDetail()
      } else {
        this.getintegralList()
      }
    },
    timeFormat,
    ...mapActions({
      fundDetail: 'wallet/fundDetail',
      billList: 'wallet/billList',
      fundList: 'wallet/fundList',
      integralList: 'wallet/integralList'
    }),
    changeIndex(index) {
      this.activeIndex = index
      if (index === 1) {
        this.refreshing2 = true
        this.onRefresh2()
      } else {
        this.refreshing = true
        this.onRefresh()
      }
    },
    handleLink (path) {
      this.$router.push(`${path}?symbol=${this.symbol}-TRC`)
    },
    loadFundList () {
      this.fundList({ currency: this.currency.name })
    },
    loadDetail () {
      this.fundDetail({
        currency: this.currency.name,
        coin_symbol: this.symbol
      })
        .then(({ data }) => {
          this.detailInfo = data
          console.log(this.detailInfo)
        })
    },
    loadBillList () {
      if (this.refreshing) {
        this.list = []
        this.offset = 0
        this.finished = false
        if (this.loading) {
          this.loading = false
          return
        }
      }
      if (this.loading) {
        this.refreshing = false
      }
      this.billList({
        coin_symbol: this.symbol,
        limit_begin: this.offset,
        limit_end: this.limit
      }).then(({ data }) => {
        if (data.list.length < this.limit) {
          this.finished = true
        } else {
          this.finished = false
          this.offset += this.limit
        }
        this.list = this.list.concat(data.list)
      }).finally(() => {
        this.loading = false
        this.refreshing = false
      })
    },
    onCopy () {
      this.$toast('复制成功')
    },
    onLoad () {
      this.loadBillList()
    },
    onRefresh () {
      this.loadBillList()
    }
  }
}
</script>
<style scoped lang="less">
.van-ellipsis {
  display: inline-block;
  width: 80%;
}
.detail {
  &-info {
    background-color: #fff;
    padding: 10px;
  }
  &-title {
    font-size: 16px;
    color: #727272;
  }
  &-amount {
    margin-top: 6px;
    font-size: 28px;
  }
  &-price {
    font-size: 18px;
    color: #727272;
  }
}
.copy {
  &-wrap {
    margin-top: 10px;
    display: flex;
  }
}
.bill {
  &-title {
    font-size: 16px;
    padding: 10px 10px;
    border-left: 2px solid @themeColor;
    background-color: #eee;
  }
}
.btn {
  &-group {
    margin-top: 20px;
  }
}
.van-list {
  min-height: 300px;
}
.my-swipe {
  margin: 10px 15px;
  overflow: visible;
  .van-swipe-item {
    transition: .3s;
    border-radius: 5px;overflow: hidden;
    box-shadow: 2px 2px 10px rgba(0, 0, 0, .1);
  }
  .van-swipe-item:not(.scale) {
    transform: scale(.94);
  }
}
.detail-info{
  background: #1678FF;
  color: #fff;
  text-align: center;
  .detail-title{
    color: #fff;
  }
  .detail-amount{
    margin-top: 10px;
  }
  .van-row{
    width: 100%;
    div{
      width: 100%;
    }
  }
  >ul{
    overflow: hidden;
    width: fit-content;
    margin: auto;
    margin-bottom: 12px;
    li{
      float: left;
      width: 85px;
      line-height: 33px;
      border: 1px solid #fff;
      border-radius:  0  4px 4px 0;
      font-size: 14px;
    }
    li:first-child{
      border-right: 0;
      border-radius: 4px 0 0 4px;
    }
    li.tab{
      background: #fff;
      color: #1678FF;
    }
  }
}
.van-nav-bar {
  background:#1678FF !important;
}
.van-hairline--bottom:after {
  border-bottom-width: 0px;
}
.wellet /deep/ .van-ellipsis,.wellet /deep/ .van-icon {
  color: #fff !important;
}
.van-nav-bar__content ,.van-nav-bar__title .van-ellipsis{
  color: #fff !important;
}
.btn-group{
  ul{
    width: 100%;
    overflow: hidden;
    li{
      width: 46%;
      float: left;
      text-align: c;
    }
    li:last-child{
      float: right;
    }
  }
}
.bill-title{
  background: #fff;
  border-left:none;
}

</style>
