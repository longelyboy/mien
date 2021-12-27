<template>
  <div>
    <van-nav-bar :border="false" :title="$t('buyPackage')" left-arrow @click-left="$router.back()" />
    <van-notice-bar
      :text="userInfo.vip_deadline > 0 ? `${$t('tip1')}：${ format(userInfo.vip_deadline, '{y}-{m}-{d}') }` : $t('tip2')"
    />
    <van-cell-group>
      <van-cell v-for="item in list" :key="item.id">
        <van-row type="flex" justify="space-between" align="center">
          <van-col>
            <div class="name">{{ item.package_name }}</div>
          </van-col>
          <van-col>
            <div class="time">{{ item.period }}{{ $t('day') }}</div>
          </van-col>
        </van-row>
        <van-row type="flex" justify="space-between" align="center">
          <van-col>
            <div class="price">{{ `${$t('price')}：${item.price} ${item.coin_symbol}` }}</div>
          </van-col>
          <van-col>
            <van-button class="btn" size="mini" type="primary" @click="buyItem(item.id)">{{ $t('buy') }}</van-button>
          </van-col>
        </van-row>
      </van-cell>
    </van-cell-group>
    <password-confirm :show="showPwd" @close="showPwd = false" @confrim="configBuy" />
  </div>
</template>

<script>
import { NoticeBar } from 'vant'
import { mapState, mapActions } from 'vuex'
import { format } from '@/utils/time'
import PasswordConfirm from '@/components/common/PasswordConfirm'
export default {
  components: { PasswordConfirm, [NoticeBar.name]: NoticeBar },
  i18n: {
    messages: {
      zh: {
        price: '售价',
        buy: '购买',
        day: '天',
        tip1: '您的vip身份到期时间为',
        tip2: '您的vip身份已到期！'
      },
      en: {
        price: 'price',
        buy: 'Buy',
        day: ' day',
        tip1: 'Your VIP status expires at',
        tip2: 'Your vip status has expired!'
      },
      hk: {
        price: '售價',
        buy: '購買',
        day: '天',
        tip1: '您的vip身份到期時間為',
        tip2: '您的vip身份已到期！'
      }
    }
  },
  data () {
    return {
      list: [],
      showPwd: false,
      package_id: ''
    }
  },
  computed: {
    ...mapState({
      userInfo: ({ user }) => user.userInfo
    })
  },
  created() {
    this.getData()
  },
  methods: {
    format,
    ...mapActions({
      getUserInfo: 'user/getUserInfo',
      packageList: 'package/packageList',
      packageBuy: 'package/packageBuy'
    }),
    getData () {
      this.packageList().then((res) => {
        this.list = res.data
      })
    },
    buyItem (id) {
      this.package_id = id
      this.showPwd = true
    },
    configBuy(password) {
      this.showPwd = false
      this.$toast.loading()
      this.packageBuy({
        password,
        package_id: this.package_id
      }).then((res) => {
        this.$toast.success(res.msg)
        this.getData()
        this.getUserInfo()
      }).catch((res) => {
        this.$toast.fail(res.msg)
      })
    }
  }
}
</script>

<style scoped>
.name {
  font-size: 1.2em;
  font-weight: 500;
}
.time {
  color: #999;
}
.price {
  color:#1678FF;
}
.btn {
  padding: 0 15px
}
.tip {
  background-color: #fff;
}
</style>
