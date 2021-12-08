<template>
  <div>
    <van-nav-bar :title="$t('title')" left-arrow @click-left="$router.back()" />
    <van-form @submit="onSubmit">
      <van-field
        v-model="username"
        :rules="[{ required: true, message: $t('phone_please') }]"
      >
        <div slot="label" class="slot-label">{{ $t('phone') }}</div>
        <div slot="input" class="slot-inp">
          <span class="tel-area" @click="showPicker=true">{{ area_num }} -</span>
          <input
            v-model="username"
            type="number"
            class="van-field__control"
            :placeholder="$t('phone')"
          />
        </div>
      </van-field>
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
    <van-popup v-model="showPicker" position="bottom" round>
      <van-picker show-toolbar :columns="areaNums" :visible-item-count="10" @confirm="confirmArea" @cancel="showPicker=false" />
    </van-popup>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
import { areaNums } from '@/constants/area_nums'
import { isPhone } from '@/utils/validator'
export default {
  i18n: {
    messages: {
      zh: {
        title: '绑定手机',
        phone: '手机',
        phone_please: '请填写手机',
        code: '验证码',
        code_please: '请填写验证码',
        send: '发送验证码'
      },
      en: {
        title: 'Binding phone',
        phone: 'phone',
        phone_please: 'Please fill in the phone address',
        code: 'Code',
        code_please: 'Please fill in the code',
        send: 'Send Code'
      }
    }
  },
  data () {
    return {
      areaNums,
      area_num: '86',
      showPicker: false,
      username: '',
      verification_code: '',
      times: 60
    }
  },
  methods: {
    ...mapActions({
      bindPhone: 'user/bindPhone',
      getUserInfo: 'user/getUserInfo',
      getCode: 'user/getCode'
    }),
    handleGetCode () {
      if (isPhone(this.username)) {
        const username = `${this.area_num}-${this.username}`
        this.getCode(username)
          .then(() => {
            this.getTime()
          })
          .catch(({ msg }) => {
            this.$toast(msg)
          })
      } else {
        this.$toast('手机号格式不正确')
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
      this.bindPhone().then(() => {
        this.getUserInfo()
        this.$router.back()
      })
    },
    confirmArea (values) {
      this.area_num = values.phone_code
      this.showPicker = false
    }
  }
}
</script>

<style scoped lang="less">
.slot-inp {
  display: flex;
  align-items: center;
}
.tel-area {
  flex-shrink: 0;
  color: #666;
  margin-right: 5px;
}
.slot-label {
  height: 100%;
  display: flex;align-items: center;
}
.select {
  border: none;
  -moz-appearance: none;
  -webkit-appearance: none;
  border-radius: 0;
  outline: medium;
  background-color: transparent;
  color: #646566;
}
</style>
