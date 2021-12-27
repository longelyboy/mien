<template>
  <div>
    <van-nav-bar
      :title="`${symbol}${$t('title')}`"
      left-arrow
      @click-left="$router.back()"
    />
    <van-tabs
      v-model="activeSymbol"
      type="card"
      class="tab-wrap"
      @click="switchTab"
    >
      <van-tab
        title="TRC20"
        name="USDT-TRC"
      />
      <van-tab
        v-if="CHEKC_ERC"
        title="ERC20"
        name="USDT"
      />
    </van-tabs>
    <van-form @submit="onSubmit">
      <van-field
        v-model="form.to_address"
        :label="$t('address')"
        :placeholder="$t('address_please')"
        :rules="[{ required: true, message: $t('address_please') }]"
      />
      <!-- <van-field
        v-model="form.address_memo"
        label="Memo"
        :placeholder="$t('memo_please')"
        :rules="[{ required: true, message: $t('memo_please') }]"
      /> -->
      <van-field
        v-model="form.amount"
        type="number"
        :label="$t('number')"
        :placeholder="symbol"
        :rules="[{ required: true, message: $t('number_please') }]"
      />
      <van-row
        style="background:#fff"
        type="flex"
        justify="end"
        class="balance-wrap"
      >
        <van-col span="18">{{ $t('balance') }}: {{ detailInfo.cloud_balance }} {{ symbol }}</van-col>
        <van-col
          span="6"
          class="balance-link"
          @click="pickAll"
        >
          {{ $t('extract_all') }}
        </van-col>
      </van-row>
      <van-field
        v-model="form.fee"
        type="number"
        name="fee"
        :label="$t('fee')"
        :placeholder="$t('fee_please') + `(${detailInfo.min_fee} ~ ${detailInfo.max_fee})`"
        :rules="[{ required: true, message: $t('fee_please') }]"
        readonly
      />
      <van-field
        v-if="userInfo.has_paypwd === 1"
        v-model="form.passWord_pay"
        type="password"
        name="paypass"
        :label="$t('pay_pwd')"
        :placeholder="$t('pwd_please')"
        :rules="[{ required: true, message: $t('pwd_please') }]"
      />
      <van-field
        v-else
        center
        clearable
        :label="$t('pay_pwd')"
        :placeholder="$t('no_pay_pwd')"
        disabled
      >
        <template #button>
          <nuxt-link to="/user/settings/payPwd">
            <van-button
              plain
              size="mini"
              type="primary"
            >
              {{ $t('setting') }}
            </van-button>
          </nuxt-link>
        </template>
      </van-field>
      <!-- <van-field
        v-model="form.memo"
        rows="1"
        autosize
        :label="$t('memo')"
        type="textarea"
        :placeholder="$t('memo_please')"
      /> -->
      <p class="tips">{{ $t('tips') }}：20 USDT</p>
      <div style="padding: 16px;">
        <van-button
          round
          block
          type="info"
          native-type="submit"
        >
          {{ $t('submit') }}
        </van-button>
      </div>
    </van-form>
  </div>
</template>
<script>
import { mapState, mapActions } from 'vuex'
import { Slider } from 'vant'
import { CHEKC_ERC } from '@/config/index'
export default {
  components: {
    [Slider.name]: Slider
  },
  i18n: {
    messages: {
      zh: {
        title: '提币',
        address: '收款地址',
        address_please: '请输入收款地址',
        memo_please: '请输入memo',
        number: '提币数量',
        number_please: '请输入提币数量',
        balance: '当前余额',
        extract_all: '全部',
        fee: '手续费',
        fee_please: '请填写手续费',
        pay_pwd: '支付密码',
        pwd_please: '请填写支付密码',
        no_pay_pwd: '还未设置支付密码',
        setting: '去设置',
        memo: '备注',
        submit: '发送',
        tips: '最小提币金额'
      },
      en: {
        title: 'withdraw coins',
        address: 'address',
        address_please: 'Please enter the Receipt address',
        memo_please: 'Please enter the memo',
        number: 'Number',
        number_please: 'Please enter the purchase quantity',
        balance: 'Current Balance',
        extract_all: 'Extract all',
        fee: 'Fee',
        fee_please: 'transaction fee',
        pay_pwd: 'Payment Password',
        pwd_please: 'Please fill in the payment password',
        no_pay_pwd: 'No payment password set yet',
        setting: 'Go to Settings',
        memo: 'notes',
        submit: 'Send',
        tips: 'Minimum withdrawal amount'
      },
      hk: {
        title: '提幣',
        address: '收款地址',
        address_please: '請輸入收款地址',
        memo_please: '請輸入memo',
        number: '提幣數量',
        number_please: '請輸入提幣數量',
        balance: '當前余額',
        extract_all: '全部',
        fee: '手續費',
        fee_please: '請填寫手續費',
        pay_pwd: '支付密碼',
        pwd_please: '請填寫支付密碼',
        no_pay_pwd: '還未設置支付密碼',
        setting: '去設置',
        memo: '備註',
        submit: '發送',
        tips: '最小提幣金額'
      },
    }
  },
  data () {
    const symbol = this.$route.query.symbol
    return {
      symbol,
      CHEKC_ERC,
      form: {
        coin_symbol: symbol,
        amount: '',
        to_address: '',
        memo: '',
        fee: '',
        address_memo: '',
        passWord_pay: ''
      },
      detailInfo: {
        min_fee: '-',
        max_fee: '-'
      },
      activeSymbol: symbol
    }
  },
  computed: {
    ...mapState({
      currency: ({ currency }) => currency,
      userInfo: ({ user }) => user.userInfo
    })
  },
  created () {
    this.loadDetail()
  },
  methods: {
    ...mapActions({
      fundDetail: 'wallet/fundDetail',
      withdraw: 'wallet/withdraw'
    }),
    pickAll () {
      if (this.detailInfo.cloud_balance > 0) {
        this.form.amount = this.detailInfo.cloud_balance - this.form.fee
      }
    },
    loadDetail () {
      this.$toast.loading()
      this.fundDetail({
        currency: this.currency.name,
        coin_symbol: this.activeSymbol
      })
        .then(({ data }) => {
          this.detailInfo = data
          this.form.fee = data.max_fee
        })
        .finally(() => {
          this.$toast.clear()
        })
    },
    onSubmit (values) {
      if (this.userInfo.has_paypwd === 0) {
        this.$router.push('/user/settings/payPwd')
        return
      }
      this.$toast.loading()
      this.withdraw(this.form)
        .then(({ msg }) => {
          this.$toast(msg)
          this.$router.push('/wallet?symbol=USDT')
        })
        .catch(({ msg }) => {
          this.$toast(msg)
        })
    },
    switchTab (name) {
      this.form = {
        coin_symbol: name,
        amount: '',
        to_address: '',
        memo: '',
        fee: '',
        address_memo: '',
        passWord_pay: ''
      }
      this.loadDetail()
    }
  }
}
</script>
<style scoped lang="less">
.custom-button {
  width: 26px;
  color: #fff;
  font-size: 10px;
  line-height: 18px;
  text-align: center;
  background-color: #ee0a24;
  border-radius: 100px;
}
.balance-wrap {
  text-align: right;
  padding: 5px 10px;
}
.balance-link {
  display: inline-block;
  text-align: center;
  color: #1296db;
}
.tab-wrap {
  padding: 10px;
  background: #fff;
  .van-tabs__wrap{
   border-radius: 10px;
 }
}
.tab-wrap  /deep/ .van-tabs__nav{
  border-radius: 14px;
  overflow: hidden;
}
.tab-wrap  /deep/ .van-tabs__nav  div:first-child{
   border-top-left-radius: 50px;
    border-bottom-left-radius: 50px;
}
.tab-wrap  /deep/ .van-tabs__nav  div:last-child{
    border-top-right-radius: 50px;
    border-bottom-right-radius: 50px;
}
.tips {
  padding: 10px;
  font-size: 12px;
  color: #888;
}
</style>
