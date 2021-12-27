<template>
  <div style="overflow-x: hidden">
    <div safe-area-inset-top>
      <van-row type="flex" justify="space-between" align="center" class="page-header">
        <van-col class="page-header-left" style="width:100%;margin:auto;">
          <h2 class="page-title" >{{ $t('nav.position') }}</h2>
        </van-col>
      </van-row>
    </div>
    <van-row class="head" type="flex" justify="space-between" align="center">
      <van-col>{{ $t('asset_name') }}</van-col>
      <van-col>{{ $t('income') }}</van-col>
      <van-col>{{ $t('up_down') }}</van-col>
    </van-row>
    <div>
      <template v-if="robotData.length">
        <van-swipe-cell v-for="item in robotData" :key="item.id" class="ticker-item" disabled>
          <van-cell v-if="item.status == 1 && item.values_str !==undefined">
            <van-row type="flex" justify="space-between" align="center">
              <van-col class="left">
                <p>{{ item.stock }} <i>/USDT</i> </p>
                <p> {{ item.price | numberFormat(5) }}（{{ item.platform }}）</p>
              </van-col>

              <van-col class="right">
                <p class="top">{{ item.first_order_value| numberFormat(5) }} USDT</p>
                <p class="bottom">{{ item.revenue | numberFormat(5) }}  USDT</p>
              </van-col>
              <van-col class="right">
                <p class="" :class=" item.rate < 0 ? 'hq-red' : 'hq-green'">
                  {{ item.rate }}%
                </p>
              </van-col>
            </van-row>
          </van-cell>
          <template #right>
            <van-button square type="danger" :text="$t('actions.del')" />
          </template>
        </van-swipe-cell>
      </template>
      <van-empty v-else :description="$t('empty.default')" />
    </div>
    <ticker-drawer ref="drawer" />
  </div>
</template>

<script>
import { SwipeCell } from 'vant'
import { mapState, mapActions } from 'vuex'
import TickerDrawer from '../ticker/components/TickerDrawer'
const timer = null
let isDestroy = false
export default {
  layout: 'navigation',
  components: {
    [SwipeCell.name]: SwipeCell,
    TickerDrawer
  },
  data () {
    return {
      isLoading: false
    }
  },
  computed: {
    ...mapState({
      tickerList: ({ ticker }) => ticker.list,
      robotData: ({ robot }) => robot.robotList
    })
  },
  async created () {
    isDestroy = false
    await this.robotList()
    const timer = setInterval(async () => {
      await this.robotList()
    }, 4000)
    this.$once('hook:beforeDestroy', () => {
      clearTimeout(timer)
    })

    // this.$once('hook:beforeDestroy', () => {
    //   isDestroy = true
    // })
  },
  methods: {
    ...mapActions({
      robotList: 'robot/robotList'
    }),
    handleLink (path) {
      this.$router.push(path)
    },
    getDeal (values) {
      if (values) {
        const valueJson = JSON.parse(values)
        return Number(valueJson.deal_amount).toFixed(6) || '-'
      }
      return '-'
    },

    getRate({price,first_order_value}) {
      // alert(first_order_value)
      const val = ((price - first_order_value) / first_order_value).toFixed(5)
      return {
        str: val < 0 ? '' : '+',
        val
      }
    }
  }
}
</script>

<style scoped lang="less">
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
/deep/ .ticker-item {
  .left {
    display: flex;
    align-items: center;
    line-height: 20px;
    margin-top: -24px;
    font-size: 12px;
    p{
      color: #8F939A;
      margin-top: 48px;
      margin-left: -72px;
    }
    p:first-child{
      font-size: 16px;
      color:#0C2233;
      font-weight: 700;
      margin: 0;
      i{
        color: #8F939A;
        font-size: 12px;
        font-style: initial;
        font-weight: 400;
      }
    }
  }
  .van-image__img {
    width: 32px;
    margin-right: 10px;
    border-radius: 50%;
  }
  .right {
    text-align: right;
    line-height: 24px;
    .top{
      color:#0C2233;
      font-size: 16px;
      font-weight: 700;
    }
    .bottom{
      color:#8F939A;
      font-size: 12px;

    }
  }
}
.hq-red {
  background: #E4505E;
  border-radius: 4px;
  color: #fff;
  width: 84px;
  line-height: 33px;
  text-align: center;
  font-size: 16px;
}
.hq-green {
  font-size: 16px;
  text-align: center;
  width: 84px;
  line-height: 33px;
  color: #47915b;
  background: #02B999;
  border-radius: 4px;
  color: #fff;
}
.head {
  padding: 10px 16px;
}
.page-title{
  text-align: center;
}
</style>
