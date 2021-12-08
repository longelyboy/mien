<template>
  <div>
    <van-nav-bar
      :border="false"
      :title="robot.market_name"
      :right-text="$t('pageRobot.order')"
      left-arrow
      @click-left="$router.back()"
      @click-right="$router.push('/robot/order?id=' + robot.id)"
    />
    <div class="top">
      <h3 class="title">
        {{ robot.market_name }}
        <van-tag
          v-if="robot.recycle_status == 1"
          round
          color="#ff8447"
          type="primary"
        >
          {{ $t('cycle_strategy') }}
        </van-tag>
        <van-tag
          v-if="robot.recycle_status == 0"
          round
          color="#ff8447"
          type="primary"
        >
          {{ $t('single_strategy') }}
        </van-tag>
      </h3>
      <van-row
        v-if="robot.values"
        type="flex"
      >
        <van-col :span="8">
          <div class="label">{{ $t('position_amount') }}({{ robot.money }})</div>
          <div class="value">{{ Number(robot.values.deal_money || 0) | numberFormat(6) }}</div>
        </van-col>
        <van-col :span="8">
          <div class="label">{{ $t('average_price') }}</div>
          <div class="value">{{ Number(robot.values.base_price || 0) | numberFormat(6) }}</div>
        </van-col>
        <van-col
          :span="8"
          @click="$router.push('/robot/order?id=' + robot.id)"
        >
          <div class="label">{{ $t('number_calls') }}</div>
          <div v-if="robot.values.order_count" class="value">{{ robot.values.order_count - 1 }}</div>
          <div v-else class="value">0</div>
        </van-col>
        <van-col :span="8">
          <div class="label">{{ $t('number_positions') }}({{ robot.stock }})</div>
          <div class="value">{{ Number(robot.values.deal_amount || 0) | numberFormat(6) }}</div>
        </van-col>
        <van-col :span="8">
          <div class="label">{{ $t('now_price') }}(USDT)</div>
          <div class="value">{{ Number(last || 0) | numberFormat(6) }}</div>
        </van-col>
        <van-col :span="8">
          <div class="label">{{ $t('profit_loss') }}</div>
          <div class="value">{{ Number(robot.revenue) | numberFormat(6) }}{{ robot.money }}</div>
        </van-col>
      </van-row>
    </div>
    <div class="title-block">{{ $t('latest_log') }}</div>
    <nuxt-link
      class="link"
      :to="'/robot/log?id=' + robot.id"
    >
      {{ $t('all_log') }}
      <van-icon name="arrow" />
    </nuxt-link>
    <div class="new-msg">
      <p
        v-if="robot.show_msg"
        class="van-ellipsis"
      >
        {{ robot.show_msg }}
      </p>
      <span
        v-else
        style="color: #888"
      >{{ $t('empty.log') }}</span>
    </div>
    <div class="title-block">{{ $t('pageRobot.account_related') }}</div>
    <van-row class="block1">
      <van-col :span="24">
        {{ $t('pageRobot.available', [robot.stock]) }}：<span>{{
          Number(account[robot.stock] || 0) | numberFormat(8)
        }}</span>
      </van-col>
      <van-col :span="24">
        {{ $t('pageRobot.available', [robot.money]) }}：<span>{{
          Number(account[robot.money] || 0) | numberFormat(7)
        }}</span>
      </van-col>
    </van-row>
    <div class="title-block">{{ $t('pageRobot.strategy_related') }}</div>
    <van-row class="block1">
      <van-col :span="12">
        {{ $t('first_order_amount') }} <span>{{ robot.first_order_value }}</span>
      </van-col>
      <van-col :span="12">
        {{ $t('number_of_orders') }} <span>{{ robot.max_order_count }}</span>
      </van-col>
      <van-col :span="12">
        {{ $t('take_profit_ratio') }} <span>{{ robot.stop_profit_rate }}%</span>
      </van-col>
      <van-col :span="12">
        {{ $t('take_profit_retracement') }}
        <span>{{ robot.stop_profit_callback_rate }}%</span>
      </van-col>
      <van-col :span="12">
        {{ $t('cover_down') }} <span v-for="(item,index) in robot.newcover_rate" :key="index">{{ item }}%&nbsp;</span>
      </van-col>
      <van-col :span="12">
        {{ $t('cover_pullback') }} <span>{{ robot.cover_callback_rate }}%</span>
      </van-col>
    </van-row>
    <div class="title-block">{{ $t('pageRobot.strategic_operations') }}</div>
    <van-grid
      column-num="3"
      :border="false"
    >
      <van-grid-item
        v-if="robot.status === 0"
        @click="onEnable"
      >
        <van-image
          width="50"
          :src="icons.icon1"
        />{{ $t('pageRobot.start') }}
      </van-grid-item>
      <van-grid-item
        v-else
        @click="onDisable"
      >
        <van-image
          width="50"
          :src="icons.icon3"
        />{{ $t('pageRobot.pause') }}
      </van-grid-item>
      <van-grid-item @click="goEdit">
        <van-image
          width="50"
          :src="icons.icon2"
        />{{ $t('pageRobot.trade_setup') }}
      </van-grid-item>
      <van-grid-item @click="onClean">
        <van-image
          width="50"
          :src="icons.icon4"
        />{{
          $t('pageRobot.clearance_sell')
        }}
      </van-grid-item>
    </van-grid>
  </div>
</template>

<script>
import { Grid, GridItem, Popover } from 'vant'
import { mapGetters, mapActions } from 'vuex'
export default {
  components: {
    [Grid.name]: Grid,
    [GridItem.name]: GridItem,
    [Popover.name]: Popover
  },
  data () {
    return {
      market_id: '',
      robot: {},
      icons: {
        icon1: require('@/assets/images/jiaoyi6.png'),
        icon2: require('@/assets/images/jiaoyi3.png'),
        icon3: require('@/assets/images/jiaoyi5.png'),
        icon4: require('@/assets/images/jiaoyi4.png')
      },
      showPopover: false,
      account: {},
      last: ''
    }
  },
  computed: {
    ...mapGetters({
      robotFind: 'robot/robot'
    })
  },
  created () {
    this.market_id = JSON.parse(this.$route.query.market_id)
    this.robotList().then(() => {
      this.robot = this.robotFind(this.market_id)

      console.log(this.robot)
      const obj = JSON.parse(this.robot.cover_rate)
      const arr = []
      for (const key in obj) {
        // console.log(obj[key])
        arr.push(obj[key])
      }
      this.robot.newcover_rate = arr
      this.apiAccountBalance({ platform: this.robot.platform }).then((res) => {
        this.account = res.data.free
      }).catch((res) => {
        this.$toast(res.msg)
      })
      this.publicTicker({
        exchange: this.robot.platform,
        market: this.robot.market_name,
        currency: 'USD'
      }).then((res) => {
        this.last = res.data.last
      }).catch((res) => {
        this.$toast(res.msg)
      })
    })
  },
  methods: {
    ...mapActions({
      robotList: 'robot/robotList',
      robotEnable: 'robot/robotEnable',
      robotDisable: 'robot/robotDisable',
      robotClean: 'robot/robotClean',
      apiAccountBalance: 'authorize/apiAccountBalance',
      publicTicker: 'robot/publicTicker'
    }),
    goEdit () {
      this.$router.push({
        name: 'robot-form',
        query: {
          type: 'edit',
          robot_id: this.robot.id
        }
      })
    },
    onEnable () {
      this.$dialog
        .confirm({
          message: this.$t('pageRobot.dialog_enable') + '？'
        })
        .then((res) => {
          this.$toast.loading()
          this.robotEnable({ robot_id: this.robot.id }).then((res) => {
            this.$toast(res.msg)
            this.robotList()
            this.$nextTick(() => {
              this.robot = this.robotFind(this.market_id)
              this.robot.status = 1
            })
          }).catch((res) => {
            this.$toast(res.msg)
          })
        })
    },
    onDisable () {
      this.$dialog
        .confirm({
          message: this.$t('pageRobot.dialog_pause') + '？'
        })
        .then((res) => {
          this.$toast.loading()
          this.robotDisable({ robot_id: this.robot.id }).then((res) => {
            this.$toast(res.msg)
            this.robotList()
            this.$nextTick(() => {
              this.robot = this.robotFind(this.market_id)
              this.robot.status = 0
            })
          }).catch((res) => {
            this.$toast(res.msg)
          })
        })
    },
    onClean () {
      this.$dialog
        .confirm({
          message: this.$t('pageRobot.dialog_sell') + '？'
        })
        .then((res) => {
          this.$toast.loading()
          this.robotClean({ robot_id: this.robot.id }).then((res) => {
            this.$toast(res.msg)
            this.$router.back()
          })
        })
    }
  }
}
</script>

<style scoped lang="less">
/deep/ .van-popover__action {
  width: 134px;
}
.top {
  padding: 15px;
  background: linear-gradient(to bottom right, rgb(21, 69, 212), rgb(25, 137, 250));
  .title {
    color: #ffffff;
    font-size: 1.5em;
    margin-bottom: 15px;
    .van-tag {
      font-weight: normal;
    }
  }
  .van-col {
    padding: 10px 10px 10px 0;
    color: #ffffff;
  }
  .label {
    opacity: 0.8;
    margin-bottom: 5px;
  }
  .value {
    font-size: 16px;
  }
}
.title-block {
  display: flex;
  align-items: center;
  padding: 10px 15px;
  font-weight: 500;
  font-size: 1em;
  &::before {
    content: '';
    width: 0.25em;
    height: 1em;
    margin-right: 10px;
    background-color: @themeColor;
  }
}
.block1 {
  background-color: #fff;
  padding: 10px 15px;
  color: #888888;
  .van-col {
    margin: 10px 0;
  }
  span {
    color: @themeColor;
    font-size: 16px;
  }
}
.new-msg {
  background: #fff;
  padding: 10px 15px;
}
.link {
  float: right;
  margin-top: -39px;
  line-height: 39px;
  padding: 0 15px;
  font-size: 12px;
  display: flex;
  align-items: center;
}
</style>
