<template>
  <div>
    <van-nav-bar
      :title="$t('pageUser.google_valid')"
      left-arrow
      @click-left="$router.back()"
    />
    <div class="container">
      <div v-if="step === 0">
        <van-button
          v-if="!userInfo.is_google_check"
          block
          type="primary"
          class="kaiqi"
          @click="handleClick"
        >{{ $t('open') }}</van-button>
        <van-button
          v-else
          block
          type="primary"
          class="kaiqi"
          @click="handleClose"
        >{{ $t('关闭二步验证') }}</van-button>
        <p>
          {{ $t('tip1') }}
        </p>
        <a
          class="how"
          @click="goDetail"
        >{{ $t('help') }}？</a>
      </div>
      <div
        v-else
        class="google"
      >
        <div class="qr">
          <qrcode-vue
            v-if="googleInfo.vcode"
            :value="googleInfo.vcode"
            size="160"
          ></qrcode-vue>
        </div>
        <div class="fuzhi">
          <a href="#">{{ googleInfo.key }}</a>
        </div>
        <div class="tixing">{{ $t('tip2') }}</div>
        <van-button
          size="small"
          type="primary"
          @click="showPop2 = true"
        >
          {{ $t('btn') }}
        </van-button>
      </div>
    </div>
    <van-dialog
      v-model="showPop"
      :title="$t('set_code')"
      show-cancel-button
      @confirm="handleSubmit"
    >
      <van-cell-group>
        <van-field
          v-model="vcode"
          input-align="center"
          :placeholder="$t('code_please')"
        />
      </van-cell-group>
    </van-dialog>
    <van-dialog
      v-model="showPop2"
      :title="$t('输入Google验证码')"
      show-cancel-button
      @confirm="checkCode"
    >
      <van-cell-group>
        <van-field
          v-model="check_num"
          input-align="center"
          :placeholder="$t('code_please')"
        />
      </van-cell-group>
    </van-dialog>
  </div>
</template>

<script>
import QrcodeVue from 'qrcode.vue'
import { mapState, mapActions } from 'vuex'
export default {
  components: { QrcodeVue },
  i18n: {
    messages: {
      zh: {
        open: '立即开启',
        close: '关闭二步验证',
        tip1: '谷歌两步验证可以为您的账户增加一层保护，当您登录时，再输入密码的同时，还需要来自两步验证的验证码。',
        help: '如何使用谷歌两步验证',
        set_code: '输入手机验证码',
        code_please: '请输入验证码',
        google: '输入Google验证码',
        tip2: '请将上方的16位回复秘钥备份在安全的地方，遗失秘钥将无法回复两步验证。',
        btn: '我已设备并备份秘钥'
      },
      en: {
        open: 'Open Now',
        close: 'Close two-step verification',
        tip1: 'Google Two-Step Verification adds an extra layer of protection to your account by requiring a verification code from Two-Step Verification when you sign in, along with your password.',
        help: 'How to use Google Two Step Verification',
        set_code: 'Enter cell phone verification code',
        code_please: 'verification code',
        google: 'Enter Google Authentication Code',
        tip2: 'Please backup the above 16-bit reply key in a safe place, losing the key will not be able to reply to the two-step verification.',
        btn: 'I have the device and backed up the secret key'
      }
    }
  },
  data () {
    return {
      step: 0,
      showPop: false,
      showPop2: false,
      vcode: '',
      check_num: '',
      googleInfo: {
        key: '',
        vcode: ''
      }
    }
  },
  computed: {
    ...mapState({
      userInfo: ({ user }) => user.userInfo,
      googleUrl: index => index.initInfo.google_auth_help
    })
  },
  methods: {
    ...mapActions({
      getUserInfo: 'user/getUserInfo',
      getCode: 'user/getCode',
      checkOpenGoogle: 'user/checkOpenGoogle',
      checkConfirmGoogle: 'user/checkConfirmGoogle',
      checkCloseGoogle: 'user/checkCloseGoogle'
    }),
    handleClick () {
      this.$toast.loading()
      this.getCode(this.userInfo.mobile)
        .then((res) => {
          this.$toast(res.msg)
          this.showPop = true
        })
        .catch((res) => {
          this.$toast(res.msg)
        })
    },
    handleSubmit () {
      this.checkOpenGoogle({ vcode: this.vcode })
        .then((res) => {
          const vcode = decodeURIComponent(res.data.vcode_img_str)
          this.googleInfo = {
            key: res.data.key,
            vcode
          }
          this.step = 1
        })
        .catch((res) => {
          this.$toast(res.msg)
        })
    },
    checkCode () {
      this.$toast.loading()
      const payload = {
        check_num: this.check_num
      }
      const promise = !this.userInfo.is_google_check ? this.checkConfirmGoogle(payload) : this.checkCloseGoogle(payload)
      promise.then((res) => {
        this.$toast(res.msg)
        this.getUserInfo()
        this.$touter.back()
      })
        .catch((res) => {
          this.$toast(res.msg)
        })
    },
    handleClose () {
      this.showPop2 = true
    },
    goDetail () {
      this.$router.push({
        name: 'common-article',
        params: {
          url: this.googleUrl,
          title: '如何使用谷歌两步验证？'
        }
      })
    }
  }
}
</script>

<style scoped lang="less">
p {
  margin: 20px 0;
  color: #888;
}
a {
  color: @themeColor;
}
/deep/ .van-dialog__content {
  padding: 30px 15px;
}
.container {
  padding: 20px;
}
.google {
  text-align: center;
  .qr {
    margin: 0 auto 20px;
    background-color: #fff;
    width: 200px;
    height: 200px;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 5px 5px 50px -15px rgba(0, 0, 0, 0.3);
  }
  .fuzhi {
    font-size: 18px;
    font-weight: 500;
    margin-bottom: 20px;
  }
  .tixing {
    margin: 20px;
    color: #888;
  }
}
</style>
