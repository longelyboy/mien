<template>
  <div>
    <van-nav-bar
      :title="$t('title')"
      left-arrow
      @click-left="$router.back()"
    />

    <van-cell
      :title="$t('left')"
      :value="$t('right')"
    />

    <draggable v-model="list">
      <transition-group>
        <div
          v-for="item in list"
          :key="item.id"
        >
          <van-cell
            :border="false"
            center
            :title="`${item.coin}/${item.currency}`"
            :label="item.exchange_name"
          >
            <template #right-icon>
              <img
                src="~@/assets/images/icon_sort.png"
                width="20"
                height="20"
              />
            </template>
          </van-cell>
        </div>
      </transition-group>
    </draggable>
  </div>
</template>
<script>
import { mapState, mapActions } from 'vuex'
import { SwipeCell } from 'vant'
import draggable from 'vuedraggable'
let unwatch
export default {
  components: {
    [SwipeCell.name]: SwipeCell,
    draggable
  },
  i18n: {
    messages: {
      zh: {
        title: '自定义排序',
        left: '货币',
        right: '拖动排序'
      },
      en: {
        title: 'Custom Sort',
        left: 'Currency',
        right: 'Drag Sort'
      },
      hk: {
        title: '自定義排序',
        left: '貨幣',
        right: '拖動排序'
      }
    }
  },
  data () {
    return {
      list: []
    }
  },
  computed: {
    ...mapState({
      currency: ({ currency }) => currency
    })
  },
  created () {
    this.loadTickerList()
  },
  beforeDestroy () {
    if (unwatch) {
      unwatch()
    }
  },
  methods: {
    ...mapActions({
      getTickerList: 'ticker/getTickerList',
      sortTicker: 'ticker/sortTicker'
    }),
    loadTickerList () {
      const payload = {
        currency: this.currency.name,
        order: 'price',
        order_type: 'desc'
      }
      this.getTickerList(payload)
        .then(({ data }) => {
          this.list = data.list
          unwatch = this.$watch('list', this.onSortChange)
        })
    },
    onSortChange (val, old) {
      const ids = val.map((item) => {
        return item.id
      })
      this.sortTicker({ ids: ids.join(',') })
    }
  }
}
</script>
<style lang="less" scoped>
.delete-button {
  height: 100%;
}
</style>
