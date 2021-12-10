<template>
  <div style="overflow-x: hidden">
    <div safe-area-inset-top>
      <van-row type="flex" justify="space-between" align="center" class="page-header">
        <div>
          <van-col class="page-header-right">
            <van-icon
              class="sort-btn"
              name="descending"
              color="@themeColor"
              size="18"
              @click="handleLink('/ticker/rearrange')"
            />
            <van-icon
              name="plus"
              color="@themeColor"
              size="18"
              @click="handleLink('/ticker/subscribe')"
            />
          </van-col>
        </div>
        <div>
          <van-col class="page-header-left" style="width:100%;margin:auto;">
            <h2 class="page-title" >{{ $t('nav.ticker') }}</h2>
          </van-col>
        </div>
        <div></div>
      </van-row>
    </div>
    <van-row class="head" type="flex" justify="space-between" align="center">
      <van-col>{{ $t('asset_name') }}</van-col>
      <van-col>{{ $t('price_') }}</van-col>
      <van-col>{{ $t('up_down') }}</van-col>
    </van-row>
    <div>
      <template v-if="tickerList.length > 0">
        <van-swipe-cell v-for="item in tickerList" :key="item.id" class="ticker-item" disabled>
          <van-cell>
            <van-row type="flex" justify="space-between" align="center">
              <van-col class="left">
                <!-- <van-image :src="item.img_url" /> -->
                <p>{{ item.coin }} <i>/USDT</i> </p>
                <p>24H {{ item.volume }}</p>
              </van-col>

              <van-col class="right">
                <p class="top">{{ item.price_usd }}</p>
                <p class="bottom">￥{{ item.price_cny }}</p>
              </van-col>
              <van-col class="right">
                <p class="" :class="item.change < 0 ? 'hq-red' : 'hq-green'">
                  {{ item.change > 0 ? '+' + item.change + '%' : '' + item.change + '%' }}
                  <img
                    v-if="item.change >= 0"
                    src="../../assets/images/icon-caret-up.png"
                    width="8"
                    height="8"
                  />
                  <img v-else src="../../assets/images/icon-caret-down.png" width="8" height="8" />
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
import TickerDrawer from './components/TickerDrawer'
let timer = null
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
      currency: ({ currency }) => currency,
      tickerList: ({ ticker }) => ticker.list
    })
  },
  created () {
    isDestroy = false
    this.loadData()
    this.$once('hook:beforeDestroy', () => {
      isDestroy = true
      clearTimeout(timer)
    })
  },
  methods: {
    ...mapActions({
      getTickerList: 'ticker/getTickerList',
    }),
    loadData () {
      this.getTickerList({
        currency: this.currency.name,
        order: 'price',
        order_type: 'desc'
      }).finally(() => {
        if (isDestroy) {
          return
        }
        clearTimeout(timer)
        timer = setTimeout(() => {
          this.loadData()
        }, 1000)
      })
    },
    handleLink (path) {
      this.$router.push(path)
    }
  }
}
</script>

<style scoped lang="less">
.page-header {
  display: flex;
  justify-content: space-between;
  background-color: #fff;
  height: 46px;
  padding: 0 15px;
  div{
    flex: 1;
  }
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
