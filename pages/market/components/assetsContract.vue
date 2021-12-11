<template>
  <van-pull-refresh
    v-model="isLoading"
    @refresh="onLoad"
  >
    <van-list
      :immediate-check="false"
      :finished="finished"
      @load="onLoad"
    >
      <van-empty
        v-if="market.length === 0 && finished"
        :description="$t('empty.default')"
      />
      <template v-else>
        <van-cell
          v-for="item in market"
          :key="item.id"
          @click="goDetail(item)"
        >
          <div class="asset-item">
            <div class="center">
              <div class="name">
                {{ item.market_name }}
                <van-tag
                  v-if="findRobot(item.id) && findRobot(item.id).recycle_status == 1"
                  round
                  type="primary"
                >
                  {{ $t('cycle_strategy') }}
                </van-tag>
                <van-tag
                  v-if="findRobot(item.id) && findRobot(item.id).recycle_status == 0"
                  round
                  type="primary"
                >
                  {{ $t('single_strategy') }}
                </van-tag>
              </div>
              <div
                v-if="findRobot(item.id)"
                class="info"
              >
                <p>
                  {{ $t('position_amount') }}：{{ Number(findRobot(item.id).first_order_value) | numberFormat(5) }} {{ item.money }}
                </p>
                <p>
                  {{ $t('average_price') }}：{{ Number(findRobot(item.id).price) | numberFormat(5) }} {{ item.money }}
                </p>
                <p>
                  {{ $t('expected_return') }}：{{ Number(findRobot(item.id).revenue) | numberFormat(5) }} {{ item.money }}
                </p>
                <p >
                  {{ $t('revue_rate') }}：
                  <span v-if="Number(findRobot(item.id).rate) >=0" style="color:green">{{ Number(findRobot(item.id).rate) | numberFormat(5) }}%</span>
                  <span v-else style="color:red">{{ Number(findRobot(item.id).rate) | numberFormat(5) }}%</span>
                </p>
                <p
                  class="van-ellipsis"
                >
                  {{ $t('number_positions') }}：{{ getDeal(findRobot(item.id).values_str) }} {{ item.stock }}
                </p>
              </div>
            </div>
            <div class="right">
              <template v-if="findRobot(item.id)">
                <span v-if="findRobot(item.id) && findRobot(item.id).status === 0">{{ $t('status.disabled') }}</span>
                <van-icon name="arrow" />
              </template>
              <van-button
                v-else
                size="small"
                style="border: none"
                @click="addRobot(item)"
              >
                <span style="display: inline-block; vertical-align: middle">{{ $t('add_robot') }}</span>
                <van-icon
                  style="vertical-align: middle"
                  name="plus"
                />
              </van-button>
            </div>
          </div>
        </van-cell>
      </template>
    </van-list>
  </van-pull-refresh>
</template>

<script>
import { mapState, mapActions, mapGetters } from 'vuex'
export default {
  props: {
    platform: {
      type: String,
      required: true
    }
  },
  data () {
    return {
      finished: false,
      isLoading: false
    }
  },
  computed: {
    ...mapState({
      robotData: ({ robot }) => robot.robotList
    }),
    ...mapGetters({
      markets: 'robot/markets'
    }),
    market () {
      return this.markets(this.platform) || []
    }
  },
  methods: {
    ...mapActions({
      marketList: 'robot/marketList',
      robotList: 'robot/robotList'
    }),
    loadData () {
      this.finished = false
      this.marketList({
        platform: this.platform,
        type: 'swap' // 合约
      })
      this.finished = true
      this.isLoading = false
    },
    onLoad () {
      this.loadData()
      this.robotList()
    },
    findRobot (id) {
      return this.robotData.filter(item => item.market_id === id)[0]
    },
    goDetail (item) {
      if (this.findRobot(item.id)) {
        this.$nextTick(() => {
          this.$router.push({
            name: 'robot-tract',
            query: { market_id: item.id }
          })
        })
      }
    },
    addRobot (item) {
      this.$router.push({
        name: 'robot-contract',
        query: {
          type: 'create',
          platform: this.platform,
          data: JSON.stringify(item)
        }
      })
    },
    getDeal (values) {
      if (values) {
        const valueJson = JSON.parse(values)
        return Number(valueJson.deal_amount).toFixed(6) || '-'
      }
      return '-'
    },

    getValue (values) {
      if (values) {
        const valueJson = JSON.parse(values)

        return valueJson
      }
      return '-'
    }
  }
}
</script>

<style scoped lang="less">
.asset-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  .left,
  .right {
    flex-shrink: 0;
  }
  .right {
    text-align: right;
    font-size: 12px;
    color: #888888;
  }
  .center {
    flex-grow: 1;
    min-width: 0;
  }

  .name {
    color: #333333;
    font-size: 16px;
    font-weight: 500;
  }
  .info {
    font-size: 12px;
    color: #999;
  }
  .btn {
    height: auto;
    padding: 5px;
  }
}
</style>
