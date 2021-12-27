<template>
  <div>
    <van-nav-bar
      fixed
      placeholder
      left-arrow
      :title="$t('bill')"
      @click-left="$router.back()"
    />
    <div class="total-card" type="flex" gutter="20">
      <div class="total-item s1">
        <div class="label">{{ $t('msg.Profit_today') }}<!-- 今日盈利 -->(USDT)</div>
        <div class="value">{{ Number(today_revenue).toFixed(6) }}</div>
      </div>
      <div class="total-item s2">
        <div class="label">{{ $t('msg.Profit_this_week') }}<!-- 本周盈利 -->(USDT)</div>
        <div class="value">{{ Number(week_revenue).toFixed(6) }}</div>
      </div>
    </div>

    <div class="total-card" type="flex" gutter="20">
      <div class="total-item s2">
        <div class="label">{{ $t('msg.Profit_this_month') }}<!-- 本月盈利 -->(USDT)</div>
        <div class="value">{{ Number(month_revenue).toFixed(6) }}</div>
      </div>
      <div class="total-item s2">
        <div class="label">{{ $t('msg.Cumulative_profit') }}<!-- 累计盈利 -->(USDT)</div>
        <div class="value">{{ Number(total_revenue).toFixed(6) }}</div>
      </div>
    </div>
    <van-pull-refresh
      v-model="refreshing"
      @refresh="onRefresh"
    >
      <van-list
        v-model="loading"
        :finished="finished"
        :finished-text="$t('finished_text')"
        @load="onLoad"
      >
        <van-cell
          v-for="item in orderList"
          :key="item.id"
        >
          <div class="robot-item">
            <div class="row">
              <div class="name">{{ item.market }}</div>
              <div>{{ $t('income') }}：{{ Number(item.revenue) | numberFormat(8) }}</div>
            </div>
            <div class="row">
              <div>{{ $t('platform') }}：{{ item.platform }}</div>
              <div class="time">{{ item.ctime }}</div>
            </div>
          </div>
        </van-cell>
      </van-list>
      <van-empty
        v-if="orderList.length === 0"
        :description="$t('empty.bill')"
      />
    </van-pull-refresh>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
export default {
  data () {
    return {
      loading: false,
      finished: false,
      refreshing: false,
      orderList: [],
      offset: 0,
      limit: 20,
      today_revenue: 0,
      total_revenue: 0,
      week_revenue: 0,
      month_revenue: 0

    }
  },
  methods: {
    ...mapActions({
      robotRevenue: 'robot/robotRevenue'
    }),
    loadList () {
      if (this.refreshing) {
        this.orderList = []
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
      const payload = {
        limit_begin: this.offset,
        limit_end: this.limit
      }
      this.robotRevenue(payload)
        .then(({ data }) => {
          this.total_revenue = data.total_revenue
          this.today_revenue = data.today_revenue
          this.week_revenue = data.week_revenue
          this.month_revenue = data.month_revenue
          const list = data.data
          if (list.length < this.limit) {
            this.finished = true
          } else {
            this.finished = false
            this.offset += this.limit
          }
          this.orderList = this.orderList.concat(list)
        })
        .finally(() => {
          this.loading = false
          this.refreshing = false
        })
    },
    onLoad () {
      this.loadList()
    },
    onRefresh () {
      this.loadList()
    }
  }
}
</script>

<style scoped lang="less">
.robot-item {
  font-size: 12px;
  color: #666;
  .row {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .name {
    font-weight: 500;
    font-size: 14px;
  }
}
.total-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #fff;
  margin-bottom: 10px;
  padding: 12px 5px;
}
.total-item {
  position: relative;
  width: 50%;
  margin: 0 8px;
  flex: 1;
  box-shadow: 0 0 20px -8px rgba(0, 0, 0, .2);
  padding: 15px;
  font-weight: 500;
  color: #fff;
  border-radius: 5px;
  overflow: hidden;
  &::before {
    content: "";
    position: absolute;
    top: 50%;left: 60%;
    width: 40vw;height: 40vw;
    border-radius: 50%;
    background-color: rgba(255, 255, 255, .2);
  }
  &::after {
    content: "";
    position: absolute;
    bottom: 50%;left: -30%;
    width: 20vw;height: 20vw;
    border-radius: 50%;
    background-color: rgba(255, 255, 255, .2);
  }
  &.s1 {
    // background: linear-gradient(45deg, rgb(146, 211, 217), rgb(81, 185, 195))
    background-image: url('../../assets/images/dzzd1.png');
    background-size: 100%;
  }
  &.s2 {
    background-image: url('../../assets/images/dzzd2.png');
    background-size: 100%;

    // background: linear-gradient(45deg, rgb(150, 201, 252), rgb(87, 165, 251))
  }
  .label {position: relative;}
  .value {
    position: relative;
    margin-top: 5px;
    font-size: 1.4em;
  }
}
</style>
