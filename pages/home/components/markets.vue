<template>
  <div style="background-color: #fff">
    <div class="title">{{ $t('robot') }}</div>
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
        <van-pull-refresh
          v-model="isLoading"
          @refresh="loadData"
        >
          <template v-if="robot_list[item.label] && robot_list[item.label].length > 0">
            <div
              v-for="robot in robot_list[item.label]"
              :key="robot.id"
            >
              <van-cell
                class="asset-item"
                @click="goDetail(robot)"
              >
                <div class="center">
                  <div class="name">
                    {{ robot.market_name }}
                    <van-tag
                      v-if="robot && robot.recycle_status == 1"
                      round
                      type="primary"
                    >
                      {{ $t('cycle_strategy') }}
                    </van-tag>
                    <van-tag
                      v-if="robot && robot.recycle_status == 0"
                      round
                      type="primary"
                    >
                      {{ $t('single_strategy') }}
                    </van-tag>

                    <van-tag
                      v-if="robot && robot.type == 1"
                      round
                      type="danger"
                    >
                      {{ $t('nav.spot') }}
                    </van-tag>
                    <van-tag
                      v-if="robot && robot.type == 2"
                      round
                      type="danger"
                    >
                      {{ $t('nav.contract') }}
                    </van-tag>

                  </div>
                  <div
                    v-if="robot"
                    class="info"
                  >
                    <p>{{ $t('expected_return') }}：{{ Number(robot.revenue) | numberFormat(5) }} {{ robot.money }}</p>
                    <p
                      v-if="robot.show_msg"
                      class="van-ellipsis"
                    >
                      {{ $t('number_positions') }}：{{ getDeal(robot.values_str) }} {{ robot.stock }}
                    </p>
                  </div>
                </div>
              </van-cell>
            </div>
          </template>
          <van-empty
            v-else
            :description="$t('empty.run_robot')"
          />
        </van-pull-refresh>
      </van-tab>
    </van-tabs>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
export default {
  data () {
    return {
      active: 0,
      isLoading: false,
      robot_list: {}
    }
  },
  computed: {
    ...mapState({
      platform: ({ robot }) => robot.platform,
      robots: ({ robot }) => robot.robotList
    })
  },
  watch: {
    robots (values) {
      const list = values.filter(item => item.status === 1)
      this.platform.forEach((item) => {
        this.robot_list[item.label] = []
        for (const i in list) {
          if (list[i].platform === item.label) {
            this.robot_list[item.label].push(list[i])
          }
        }
      })
      this.$forceUpdate()
    }
  },
  mounted () {
    this.loadData()
  },
  methods: {
    ...mapActions({
      robotList: 'robot/robotList'
    }),
    loadData () {
      this.robotList().then(() => {
        this.isLoading = false
      })
    },
    goDetail (item) {
      this.$nextTick(() => {

        if(item.type == 2){
            this.$router.push({
            name: 'robot-tract',
            query: { market_id: item.market_id }
          })
        }else{
          this.$router.push({
            name: 'robot',
            query: { market_id: item.market_id }
          })
        }
        
      })
    },
    getDeal (values) {
      if (values) {
        const valueJson = JSON.parse(values)
        return Number(valueJson.deal_amount).toFixed(6) || '-'
      }
      return '-'
    }
  }
}
</script>

<style scoped lang="less">
.title {
  background-color: #fff;
  padding: 10px 15px;
  font-size: 18px;
  font-weight: 600;
}
.asset-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  .left {
    flex-shrink: 0;
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
    color: #888888;
  }
}
</style>
