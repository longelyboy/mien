<template>
  <div>
    <van-nav-bar
      :title="`${$t('title')}`"
      left-arrow
      @click-left="$router.back()"
    />
    <van-form @submit="onSubmit">
      <van-field
        v-model="form.to_uid"
        type="text"
        :label="$t('to_id')"
        :placeholder="$t('to_id')"
        :rules="[{ required: true, message: $t('to_id_please') }]"
      />
      <van-field
        v-model="form.amount"
        type="number"
        :label="$t('number')"
        :placeholder="initInfo.system_balance_name"
        :rules="[{ required: true, message: $t('number_please') }]"
      />
      <van-row
        style="background:#fff"
        type="flex"
        justify="end"
        class="balance-wrap"
      >
        <van-col span="18">{{ $t('balance') }}: {{ userInfo.balance }} {{ initInfo.system_balance_name }}</van-col>
        <van-col
          span="6"
          class="balance-link"
          @click="pickAll"
        >
          {{ $t('extract_all') }}
        </van-col>
      </van-row>
      <van-field
        v-if="userInfo.has_paypwd === 1"
        v-model="form.password"
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
      <div style="margin: 16px;">
        <van-button round block type="info" native-type="submit">{{ $t('actions.submit') }}<!-- 提交 --></van-button>
      </div>
    </van-form>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
export default {
  i18n: {
    messages: {
      zh: {
        title: '转账',
        number: '转账数量',
        number_please: '请输入转账数量',
        balance: '当前余额',
        pay_pwd: '支付密码',
        pwd_please: '请填写支付密码',
        no_pay_pwd: '还未设置支付密码',
        setting: '去设置',
        extract_all: '全部',
        to_id: '对方用户id',
        to_id_please: '请输入对方用户id'
      },
      en: {
        title: 'Transfer',
        number: 'Number',
        number_please: 'Enter the transfer quantity',
        balance: 'Current Balance',
        pay_pwd: 'Payment Password',
        pwd_please: 'Please fill in the payment password',
        no_pay_pwd: 'No payment password set yet',
        setting: 'Go to Settings',
        extract_all: 'Extract all',
        to_id: 'To ID',
        to_id_please: 'Please To ID'
      },
      hk: {
        title: '轉賬',
        number: '轉賬數量',
        number_please: '請輸入轉賬數量',
        balance: '當前余額',
        pay_pwd: '支付密碼',
        pwd_please: '請填寫支付密碼',
        no_pay_pwd: '還未設置支付密碼',
        setting: '去設置',
        extract_all: '全部',
        to_id: '對方用戶id',
        to_id_please: '請輸入對方用戶id'
      },
    }
  },
  data () {
    return {
      form: {
        to_uid: '',
        amount: '',
        password: ''
      }
    }
  },
  computed: {
    ...mapState({
      currency: ({ currency }) => currency,
      userInfo: ({ user }) => user.userInfo,
      initInfo: index => index.initInfo
    })
  },
  methods: {
    ...mapActions({
      balanceTransfer: 'wallet/balanceTransfer',
      getUserInfo: 'user/getUserInfo'
    }),
    pickAll () {
      if (this.userInfo.balance > 0) {
        this.form.amount = this.userInfo.balance
      }
    },
    onSubmit() {
      if (this.userInfo.has_paypwd === 0) {
        this.$router.push('/user/settings/payPwd')
        return
      }
      this.$toast.loading()
      this.balanceTransfer(this.form)
        .then(({ msg }) => {
          this.$toast(msg)
          this.getUserInfo()
          this.$router.back()
        })
        .catch(({ msg }) => {
          this.$toast(msg)
        })
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
}
.tips {
  padding: 10px;
  font-size: 12px;
  color: #888;
}
</style>
