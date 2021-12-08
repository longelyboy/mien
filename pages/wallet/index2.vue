<template>
  <div>
    <van-nav-bar
      :title="`${$t('title')}`"
      left-arrow
      @click-left="$router.back()"
    />
    <div class="detail-info">
      <van-row>
        <van-col span="20">
          <div class="detail-title">{{ $t('total2') }}（{{ initInfo.system_balance_name }}）</div>
          <div class="detail-amount">{{ userInfo.balance | numberFormat(8) }}</div>
          <!-- <div class="detail-price">≈{{ currency.symbol }} {{ detailInfo.price }}</div> -->
        </van-col>
        <van-col span="4">
          <fire theme="two-tone" size="54" :fill="['#333' ,'#ff0000']" :stroke-width="2" stroke-linejoin="miter"/>
        </van-col>
      </van-row>
      <div class="btn-group">
        <van-button
          plain
          type="primary"
          size="small"
          style="padding: 0 10px"
          @click="handleLink('/wallet/transfer')"
        >
          {{ $t('transfer') }}
        </van-button>
      </div>
    </div>

    <div class="bill-list">
      <div class="bill-title">{{ initInfo.system_balance_name }} {{ $t('bill') }}</div>
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
            :title="`${Number(item.change).toFixed(5) > 0 ? '+'+Number(item.change).toFixed(5) : Number(item.change).toFixed(5)}`"
            :value="item.detial_type_name"
            :label="timeFormat(item.ctime)"
          />
        </van-list>
      </van-pull-refresh>
    </div>
  </div>
</template>
<script>
import { Fire } from '@icon-park/vue'
import { Swipe, SwipeItem } from 'vant'
import { mapState, mapActions } from 'vuex'
import { format as timeFormat } from '@/utils/time'
export default {
  i18n: {
    messages: {
      zh: {
        title: '资产',
        total: '总资产折合',
        total2: '燃料余额',
        receipt: '充值',
        withdraw: '提币',
        transfer: '转账'
      },
      en: {
        title: ' Assets',
        total: 'Total Assets',
        total2: 'Fuel balance',
        receipt: 'Receipt',
        withdraw: 'withdraw',
        transfer: 'transfer'
      }
    }
  },
  components: {
    [Swipe.name]: Swipe,
    [SwipeItem.name]: SwipeItem,
    Fire
  },
  data () {
    return {
      list: [],
      loading: false,
      finished: false,
      refreshing: false,
      offset: 0,
      limit: 20
    }
  },
  computed: {
    ...mapState({
      currency: ({ currency }) => currency,
      initInfo: index => index.initInfo,
      userInfo: ({ user }) => user.userInfo
    })
  },
  methods: {
    timeFormat,
    ...mapActions({
      balanceLog: 'wallet/balanceLog'
    }),
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
      this.balanceLog({
        limit_begin: this.offset,
        limit_end: this.limit
      }).then(({ data }) => {
        if (data.data.length < this.limit) {
          this.finished = true
        } else {
          this.finished = false
          this.offset += this.limit
        }
        this.list = this.list.concat(data.data)
      }).finally(() => {
        this.loading = false
        this.refreshing = false
      })
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
</style>
