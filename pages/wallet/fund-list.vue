<template>
  <div>
    <van-nav-bar :title="$t('pageUser.asset')" left-arrow @click-left="$router.back()" />
    <div class="total-fund">
      <div class="total-title">{{ $t('total') }}</div>
      <div class="total-amount">≈ {{ currency.symbol }}{{ totalPrice }}</div>
    </div>
    <div class="card-list">
      <van-card
        v-for="item in funds"
        :key="item.id"
        :desc="`${$t('balance')}：${item.cloud_balance}`"
        :title="item.coin_name"
        :thumb="item.img_url"
        class="card-item"
        @click="handleLink('/wallet/fund-detail', item)"
      >
        <template #tags>
          <van-row type="flex" justify="end" gutter="10">
            <van-col span="5">
              <van-button
                plain
                block
                type="primary"
                size="mini"
                @click.stop="handleLink('/wallet/receive', item)"
              >
                {{ $t('receipt') }}
              </van-button>
            </van-col>
            <van-col span="5">
              <van-button
                plain
                block
                type="info"
                size="mini"
                @click.stop="handleLink('/wallet/withdraw', item)"
              >
                {{ $t('withdraw') }}
              </van-button>
            </van-col>
          </van-row>
        </template>
      </van-card>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import { Card } from 'vant'
export default {
  components: {
    [Card.name]: Card
  },
  i18n: {
    messages: {
      zh: {
        total: '总资产',
        balance: '余额',
        receipt: '收款',
        withdraw: '提币'
      },
      en: {
        total: 'Total Assets',
        balance: 'Balance',
        receipt: 'Receipt',
        withdraw: 'withdraw'
      }
    }
  },
  computed: {
    ...mapState({
      currency: ({ currency }) => currency,
      totalPrice: ({ wallet }) => wallet.totalPrice,
      funds: ({ wallet }) => wallet.funds
    })
  },
  created () {
    this.loadFundList()
  },
  methods: {
    ...mapActions({
      fundList: 'wallet/fundList'
    }),
    loadFundList () {
      this.fundList({ currency: this.currency.name })
    },
    handleLink (path, item) {
      this.$router.push(`${path}?symbol=${item.coin_symbol}`)
    }
  }
}
</script>

<style scoped lang="less">
.total {
  &-fund {
    background-color: #fff;
    padding: 4px;
    border-bottom: 1px solid #eae8e8;
  }
  &-title {
    color: #264258;
    font-size: 20px;
    font-weight: 700;
    text-align: center;
  }
  &-amount {
    color: #727272;
    font-size: 16px;
    text-align: center;
  }
}
.card {
  &-list {
    padding: 8px 8px;
  }
  &-item {
    margin-bottom: 10px;
  }
}
</style>
