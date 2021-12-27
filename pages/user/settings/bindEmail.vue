<template>
  <div>
    <van-nav-bar :title="$t('title')" left-arrow @click-left="$router.back()" />
    <van-form @submit="onSubmit">
      <van-field
        v-model="username"
        :label="$t('email')"
        :placeholder="$t('email_please')"
        :rules="[{ required: true, message: $t('email_please') }]"
      />
      <van-field
        v-model="verification_code"
        clearable
        :label="$t('code')"
        :placeholder="$t('code_please')"
        :rules="[{ required: true, message: $t('code_please') }]"
      >
        <template #button>
          <van-button size="small" type="primary" block @click.prevent="handleGetCode">{{ $t('send') }}</van-button>
        </template>
      </van-field>
      <div style="margin: 15px">
        <van-button block type="info" native-type="submit" class="submit">
          {{ $t('actions.submit') }}
        </van-button>
      </div>
    </van-form>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
import { isEmail } from '@/utils/validator'
export default {
  i18n: {
    messages: {
      zh: {
        title: '绑定邮箱',
        email: '邮箱',
        email_please: '请填写邮箱',
        code: '验证码',
        code_please: '请填写验证码',
        send: '发送验证码'
      },
      en: {
        title: 'Binding Email',
        email: 'Email',
        email_please: 'Please fill in the email address',
        code: 'Code',
        code_please: 'Please fill in the code',
        send: 'Send Code'
      },
      hk: {
        title: '綁定郵箱',
        email: '郵箱',
        email_please: '請填寫郵箱',
        code: '驗證碼',
        code_please: '請填寫驗證碼',
        send: '發送驗證碼'
      }
    }
  },
  data () {
    return {
      username: '',
      verification_code: '',
      times: 60
    }
  },
  methods: {
    ...mapActions({
      bindEmail: 'user/bindEmail',
      getUserInfo: 'user/getUserInfo',
      getCode: 'user/getCode'
    }),
    handleGetCode () {
      if (isEmail(this.username)) {
        this.getCode(this.username)
          .then(() => {
            this.getTime()
          })
          .catch(({ msg }) => {
            this.$toast(msg)
          })
      } else {
        this.$toast(this.$t('msg.The_mailbox_number_format_is_incorrect'))/* '邮箱号格式不正确' */
      }
    },
    getTime () {
      this.timer = setInterval(() => {
        this.times--
        if (this.times === 0) {
          clearInterval(this.timer)
          this.times = 60
        }
      }, 1000)
    },
    onSubmit () {
      this.bindEmail().then(() => {
        this.getUserInfo()
        this.$router.back()
      })
    }
  }
}
</script>
