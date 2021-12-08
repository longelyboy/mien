<template>
  <div>
    <van-nav-bar :title="$t('title')" left-arrow @click-left="$router.back()" />
    <div v-if="has_paypwd && !vcode && !old_pwd" class="tips">{{ $t('tip1') }}</div>
    <div v-else class="tips">{{ $t('tip2') }}</div>
    <van-password-input
      :value="value"
      :focused="showKeyboard"
      :length="6"
      :info="$t('tips.password')"
      @focus="showKeyboard = true"
    />
    <div v-if="has_paypwd" class="forget-pwd" >
      <a @click="setForget">{{ $t('forget') }}？</a>
    </div>
    <van-number-keyboard
      safe-area-inset-bottom
      :show="showKeyboard"
      @blur="showKeyboard = false"
      @input="(val) => (value += val)"
      @delete="onDelete"
    />
    <van-dialog v-model="showPop" :title="$t('title2')" show-cancel-button @confirm="showPop=false">
      <van-cell-group>
        <van-field :label="$t('phone')" :value="mobile" readonly />
        <van-field v-model="vcode" :label="$t('code')" :placeholder="$t('code_please')" 
        >
            <template #button>
              <van-button
                size="small"
                type="primary"
                block
                :disabled="times !== 60"
                @click.prevent="handleGetCode"
              >
                <template v-if="times === 60">{{ $t('send') }}</template>
                <template v-else>{{ times }}s</template>
              </van-button>
            </template>
      </van-field>        
      </van-cell-group>
    </van-dialog>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import { PasswordInput, NumberKeyboard } from 'vant'
export default {
  components: {
    [PasswordInput.name]: PasswordInput,
    [NumberKeyboard.name]: NumberKeyboard
  },
  i18n: {
    messages: {
      zh: {
        title: '支付密码',
        tip1: '请输入支付密码，以验证身份',
        tip2: '请设置支付密码，用于支付验证',
        forget: '忘记支付密码',
        title2: '验证身份',
        phone: '手机号',
        code: '验证码',
        code_please: '请输入验证码',
        send: '发送'
      },
      en: {
        title: 'Payment Password',
        tip1: 'Please enter your payment password to verify your identity',
        tip2: 'Please set a payment password for payment verification',
        forget: 'Forgot your payment password',
        title2: 'Verification of identity',
        phone: 'Mobile',
        code: 'Code',
        code_please: 'Please enter the code',
        send: 'Send'
      }
    }
  },
  data () {
    return {
      showPop: false,
      showKeyboard: false,
      forgeted: false,
      value: '',
      old_pwd: '',
      pwd: '',
      vcode: '',
      times: 60      
    }
  },
  computed: {
    ...mapState({
      mobile: ({ user }) => user.userInfo.mobile,
      has_paypwd: ({ user }) => user.userInfo.has_paypwd
    })
  },
  watch: {
    value (value) {
      if (value.length === 6) {
        switch (true) {
          case Boolean(!this.has_paypwd):
          case Boolean(this.has_paypwd && this.forgeted):
          case Boolean(this.has_paypwd && !this.forgeted && this.old_pwd):
            this.pwd = value
            break
          case Boolean(this.has_paypwd && !this.forgeted && !this.old_pwd):
            this.old_pwd = value
            this.value = ''
            break
          default:
            break
        }
      }
    },
    pwd (value) {
      if (value) {
        let promise = null
        if (this.has_paypwd) {
          promise = this.forgeted
            ? this.forgetPayPwd({ new_pwd: this.pwd, vcode: this.vcode })
            : this.changePayPwd({ pwd: this.pwd, old_pwd: this.old_pwd })
        } else {
          promise = this.addPayPwd({ pwd: this.pwd })
        }
        promise.then((res) => {
          this.$toast(res.msg)
          this.getUserInfo()
          this.$router.back()
        }).catch((res) => {
          this.$toast(res.msg)
          this.$router.reload()
        })
      }
    }
  },
  mounted () {
    setTimeout(() => {
      this.showKeyboard = true
    }, 300)
  },
  methods: {
    ...mapActions({
      addPayPwd: 'user/addPayPwd',
      changePayPwd: 'user/changePayPwd',
      forgetPayPwd: 'user/forgetPayPwd',
      getUserInfo: 'user/getUserInfo',
      getCode: 'user/getCode'
    }),
    getTime () {
      this.timer = setInterval(() => {
        this.times--
        if (this.times === 0) {
          clearInterval(this.timer)
          this.times = 60
        }
      }, 1000)
    },    
    handleGetCode () {
      const username = this.mobile
     this.getCode(username)
          .then(({ msg }) => {
            this.$toast(msg)
            this.getTime()
          })
          .catch(({ msg }) => {
            this.$toast(msg)
          })
       
    },       
    onDelete () {
      const value = this.value
      this.value = value.substring(0, value.length - 1)
    },
    setForget () {
      this.showPop = true
      this.forgeted = true
      this.value = ''
    }
  }
}
</script>

<style scoped lang="less">
.tips {
  margin: 15vw 20px 10vw;
  text-align: center;
  font-size: 16px;
}
.forget-pwd {
  display: block;
  text-align: center;
  margin-top: 10px;
  font-size: 12px;
  color: @themeColor;
  a {
    display: inline-block;padding: 15px;
  }
}
/deep/ .van-dialog__content {
  padding: 30px 15px;
}
</style>
