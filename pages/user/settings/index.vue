<template>
  <div>
    <van-nav-bar
      :title="$t('title')"
      left-arrow
      @click-left="$router.back()"
    />
    <van-cell-group>
      <van-cell
        :title="$t('info')"
        is-link
        to="/user/settings/personal"
      />
      <van-cell
        v-if="userInfo.mobile"
        :title="$t('bind_phone')"
        :value="userInfo.mobile"
      />
      <van-cell
        v-else-if="!thirdLoginEnabled"
        :title="$t('bind_phone')"
        is-link
        to="/user/settings/bindPhone"
      />
      <van-cell
        v-if="userInfo.user_email"
        :title="$t('bind_email')"
        :value="userInfo.user_email"
      />
      <van-cell
        v-else-if="!thirdLoginEnabled"
        :title="$t('bind_email')"
        is-link
        to="/user/settings/bindEmail"
      />
      <van-cell
        v-if="!thirdLoginEnabled"
        :title="$t('pwd_login')"
        is-link
        to="/user/settings/changePwd"
      />
      <van-cell
        :title="$t('pwd_pay')"
        is-link
        to="/user/settings/payPwd"
      />

      <van-cell
        :title="$t('changeLang')"
        is-link
        to="/user/settings/changeLanguage"
      />
    </van-cell-group>
    <div
      v-if="!thirdLoginEnabled"
      class="btn"
    >
      <van-button
        type="danger"
        block
        @click="exitLogin"
      >
        {{ $t('exit') }}
      </van-button>
    </div>
  </div>
</template>

<script>
import { Dialog } from 'vant'
import { mapState, mapActions } from 'vuex'
export default {
  i18n: {
    messages: {
      zh: {
        title: '设置',
        info: '个人资料',
        bind_phone: '绑定手机',
        bind_email: '绑定邮箱',
        pwd_login: '登录密码',
        pwd_pay: '支付密码',
        contact: '联系我们',
        exit: '退出登录',
        tip: '提示',
        tip_msg: '是否退出当前账号',
        language: '选择语言'
      },
      en: {
        title: 'Settings',
        info: 'Personal Information',
        bind_phone: 'Binding Mobile',
        bind_email: 'Binding Email',
        pwd_login: 'Login Password',
        pwd_pay: 'Payment Password',
        contact: 'Contact Us',
        exit: 'Logout',
        tip: 'Tips',
        tip_msg: 'Whether to log out of the current account',
        language: 'Change Language'
      },
      hk: {
        title: '設置',
        info: '個人資料',
        bind_phone: '綁定手機',
        bind_email: '綁定郵箱',
        pwd_login: '登錄密碼',
        pwd_pay: '支付密碼',
        contact: '聯繫我們',
        exit: '退出登錄',
        tip: '提示',
        tip_msg: '是否退出當前賬號',
        language: '選擇語言'
      }
    }
  },
  computed: {
    ...mapState({
      userInfo: ({ user }) => user.userInfo,
      thirdLoginEnabled: ({ thirdLoginEnabled }) => thirdLoginEnabled
    })
  },
  methods: {
    ...mapActions({
      logOut: 'user/logOut'
    }),
    exitLogin () {
      Dialog.confirm({
        title: this.$t('tip'),
        message: this.$t('tip_msg') + '？'
      }).then(() => {
        this.logOut().then(() => {
          this.$router.replace('/home')
          localStorage.clear()
          localStorage.setItem('LANG','hk')
        })
      })
    }
  }
}
</script>

<style scoped lang="less">
.btn {
  margin: 15px;
}
</style>
