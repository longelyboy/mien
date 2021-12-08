<template>
  <van-grid :column-num="3">
    <van-grid-item
      v-for="item in list"
      :key="item.id"
    >
      <div class="name">{{ item.coin }}/{{ item.currency }}</div>
      <div class="price">{{ item.price }}</div>
      <div
        class="change"
        :class="{red: item.change < 0, green: item.change > 0}"
      >
        {{ item.change > 0 ? `+${item.change}` : item.change }}%
      </div>
    </van-grid-item>
  </van-grid>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import { Grid, GridItem } from 'vant'
let timer = null
let isDestroy = false
export default {
  components: {
    [Grid.name]: Grid,
    [GridItem.name]: GridItem
  },
  computed: {
    ...mapState({
      currency: ({ currency }) => currency,
      list: ({ ticker }) => ticker.list.slice(0, 3)
    })
  },
  created () {
    isDestroy = false
    this.loadData()
  },
  beforeDestroy () {
    isDestroy = true
    clearTimeout(timer)
  },
  methods: {
    ...mapActions({
      getTickerList: 'ticker/getTickerList'
    }),
    loadData () {
      this.getTickerList({
        currency: this.currency.name,
        order: 'price',
        order_type: 'desc'
      }).finally(() => {
        if (isDestroy) { return }
        clearTimeout(timer)
        timer = setTimeout(() => {
          this.loadData()
        }, 1000)
      })
    }
  }
}
</script>

<style scoped lang="less">
.name {
  font-size: 12px;
  font-weight: bold;
}
.price {
  margin: 5px 0;
  font-size: 16px;
  color: #d14b64;
}
.change {
  font-size: 12px;
  &.red {
    color: #d14b64;
  }
  &.green {
    color: #04c2ad;
  }
}
</style>
