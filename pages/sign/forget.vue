<template>
  <div>
    <van-nav-bar :title="$t('pageSign.forget_pwd')" left-arrow @click-left="$router.back()" />
    <van-form @submit="onSubmit">
      <!-- <van-field
        v-model="username"
        :label="$t('pageSign.account')"
        :placeholder="$t('pageSign.account')"
        :rules="[{ required: true }]"
      /> -->
      <van-field v-model="username" :rules="[{ required: true }]">
        <div slot="label" class="slot-label">
          <select v-model="loginType" class="select">
            <option value="phone">{{ $t('pageSign.phone') }}</option>
            <option value="email">{{ $t('pageSign.email') }}</option>
          </select>
          <van-icon name="arrow-down" size="12" />
        </div>
        <div v-if="loginType === 'email'" slot="input" class="slot-inp">
          <input
            v-model="username"
            type="text"
            class="van-field__control"
            :placeholder="$t('pageSign.email')"
          />
        </div>
        <div v-if="loginType === 'phone'" slot="input" class="slot-inp">
          <span class="tel-area" @click="showPicker=true">{{ area_num }} -</span>
          <input
            v-model="username"
            type="number"
            class="van-field__control"
            :placeholder="$t('pageSign.phone')"
          />
        </div>
      </van-field>
      <van-field
        v-model="verification_code"
        clearable
        :label="$t('pageSign.valid_code')"
        :placeholder="$t('pageSign.valid_code')"
        :rules="[{ required: true }]"
      >
        <template #button>
          <van-button size="small" type="primary" block @click.prevent="handleGetCode">
            <template v-if="times === 60">{{ $t('pageSign.send_code') }}</template>
            <template v-else>{{ times }}s</template>
          </van-button>
        </template>
      </van-field>
      <van-field
        v-model="password"
        type="password"
        :label="$t('pageSign.pwd')"
        :placeholder="$t('pageSign.pwd')"
        :rules="[{ required: true }]"
      />
      <van-field
        v-model="confirm_password"
        type="password"
        :label="$t('pageSign.confirm_pwd')"
        :placeholder="$t('pageSign.pwd')"
        :rules="[{ required: true }]"
      />
      <div style="margin: 15px">
        <van-button block type="info" native-type="submit" class="submit">{{ $t('actions.submit') }}</van-button>
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
import { isPhone, isEmailOrPhone } from '@/utils/validator'
export default {
  data () {
    return {
      areaNums,
      username: '',
      password: '',
      confirm_password: '',
      verification_code: '',
      loginType: 'phone',
      area_num: '86',
      showPicker: false,
      times: 60
    }
  },
  methods: {
    ...mapActions({
      getCode: 'user/getCode',
      login: 'user/login',
      forgetPwd: 'user/forgetPwd'
    }),
    handleGetCode () {
      if (isEmailOrPhone(this.username)) {
        const username = isPhone(this.username) ? `${this.area_num}-${this.username}` : this.username
        this.getCode(username)
          .then(() => {
            this.getTime()
          })
          .catch(({ msg }) => {
            this.$toast(msg)
          })
      } else {
        this.$toast(this.$t('pageSign.account_err'))
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
      if (this.password !== this.confirm_password) {
        this.$toast(this.$t('pageSign.pwd_err'))
        return false
      }
      const username = this.loginType === 'phone'
        ? `${this.area_num}-${this.username}`
        : this.username
      const payload = {
        username,
        password: this.password,
        verification_code: this.verification_code
      }
      this.forgetPwd(payload).then((res) => {
        this.$toast(res.msg)
        this.$router.replace('/sign/login')
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
