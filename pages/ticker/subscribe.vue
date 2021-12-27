<template>
  <div>
    <van-nav-bar
      :title="$t('title')"
      left-arrow
      @click-left="$router.back()"
    />
    <div>
      <van-search
        v-model="keyword"
        :placeholder="$t('placeholder')"
      />
      <van-index-bar :index-list="indexList">
        <div
          v-for="(tickerItem, tickerIndex) in filterList"
          :key="`${tickerItem.exchange_name}-${tickerIndex}`"
        >
          <van-index-anchor :index="tickerItem.exchange_name">{{ tickerItem.exchange_name }}（{{ tickerItem.ticker_list.count }}）</van-index-anchor>
          <van-cell
            v-for="(item, index) in tickerItem.ticker_list.list"
            :key="item.ticker_id"
            :title="`${item.coin}/${item.currency}`"
          >
            <template #right-icon>
              <van-checkbox
                v-model="item.status"
                shape="square"
                @change="onChangeCheckbox(item, index, tickerIndex)"
              />
            </template>
          </van-cell>
        </div>
      </van-index-bar>
    </div>
  </div>
</template>
<script>
import { mapActions } from 'vuex'
import { Search, IndexBar, IndexAnchor } from 'vant'
import cloneDeep from 'lodash.clonedeep'
export default {
  components: {
    [Search.name]: Search,
    [IndexBar.name]: IndexBar,
    [IndexAnchor.name]: IndexAnchor
  },
  i18n: {
    messages: {
      zh: {
        title: '自定义行情',
        placeholder: '请输入搜索关键词'
      },
      en: {
        title: 'Custom Ticker',
        placeholder: 'Please enter a search term'
      },
      hk: {
        title: '自定義行情',
        placeholder: '請輸入搜索關鍵詞'
      }
    }
  },
  data () {
    return {
      keyword: '',
      tickerAll: []
    }
  },
  computed: {
    indexList () {
      return this.tickerAll.map(item => (item.exchange_name))
    },
    filterList () {
      if (!this.keyword) {
        return this.tickerAll
      }
      return this.tickerAll.map((item) => {
        const list = item.ticker_list.list.filter((v) => {
          return new RegExp(this.keyword, 'i').test(`${v.exchange_name}|${v.coin}/${v.exchange_name}|${v.coin_name}`)
        })
        return {
          ...item,
          ticker_list: {
            count: list.length,
            list
          }
        }
      })
    }
  },
  created () {
    this.getTickerAll()
      .then(({ data }) => {
        this.tickerAll = cloneDeep(data.list)
      })
  },
  methods: {
    ...mapActions({
      getTickerAll: 'ticker/getTickerAll',
      addTicker: 'ticker/addTicker',
      removeTicker: 'ticker/removeTicker'
    }),
    onChangeCheckbox (item, index, tickerIndex) {
      if (item.status) {
        this.addTicker({ ticker_id: item.ticker_id })
      } else {
        this.removeTicker({ ticker_id: item.ticker_id })
      }
    }
  }
}
</script>
<style lang="less" scoped>
/deep/ .van-index-bar__sidebar {
  display: none;
}
</style>
