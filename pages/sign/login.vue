<template>
  <div class="container">
    <div class="card">
      <div class="form-title">
        <svg t="1614305356681" class="icon" viewBox="0 0 1433 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="32561" width="128" height="128"><path d="M1429.344088 872.228008c-15.356357 64.752637-80.774436 143.581935-304.798087 151.260113-11.107765 0.255939-22.497063 0.511879-33.963142 0.511879a1678.961666 1678.961666 0 0 1-441.802382-68.079848c-192.799058-54.259127-371.495863-135.647818-490.226094-223.179051C5.835416 620.127819-9.77688 527.733739 3.941465 470.147402c21.498899-90.346565 82.796357-119.011764 168.075324-134.112182a50.548007 50.548007 0 0 1 57.330398 44.789373 58.149404 58.149404 0 0 1-8.727529 40.438406 49.345093 49.345093 0 0 1-32.478694 22.010778c-77.93351 13.820721-82.412448 32.504288-87.531234 54.003188-6.116949 26.105806 26.592091 81.132751 113.867385 145.37351 12.105928 8.957875 24.979674 17.65981 38.390892 26.617685-1.996326-10.49351-3.864683-20.987021-5.246755-31.480531a2035.485081 2035.485081 0 0 1-2.559393-22.010778 588.353213 588.353213 0 0 1 111.384774-408.990967A500.156538 500.156538 0 0 1 700.966496 3.058218C981.680696-28.934191 1234.292764 193.732981 1263.879345 499.324479a610.466367 610.466367 0 0 1 1.126132 103.655408c0.767818 0.511879 1.510042 0.767818 2.252266 1.279696 159.219825 114.660797 175.958254 209.10239 162.086345 267.968425zM1164.523717 510.585808c-23.725571-245.957647-227.01814-425.115141-453.166087-399.265275a402.490109 402.490109 0 0 0-277.335802 163.801138 473.97395 473.97395 0 0 0-89.578747 329.393852c0.614254 5.886603 1.382072 12.029146 2.124296 17.915749a475.483991 475.483991 0 0 0 30.968653 116.708311 1797.589522 1797.589522 0 0 0 296.070557 111.589526 1706.884642 1706.884642 0 0 0 333.642443 61.169487A463.531627 463.531627 0 0 0 1164.523717 510.585808z m80.288151 209.358329a566.649562 566.649562 0 0 1-95.900447 193.234155c116.50356-7.934118 176.598102-40.182467 183.431681-68.335787 5.73304-23.290474-20.014452-69.615484-87.428858-124.898368z m-337.839847-105.702922a67.107279 67.107279 0 0 1-65.571643-68.079848v-68.335787a65.597237 65.597237 0 1 1 131.117692 0v68.335787a67.107279 67.107279 0 0 1-65.341298 68.079848z m-355.294906 0a67.107279 67.107279 0 0 1-65.54605-68.079848v-68.335787a65.597237 65.597237 0 1 1 131.117693 0v68.335787a67.107279 67.107279 0 0 1-65.366892 68.079848z" fill="#ffffff" p-id="32562"></path></svg>
        <h2>{{ $t('login') }}</h2>
      </div>
      <div class="card-shadow">
        <div class="tab">
          <span :class="{ active: active === 1 }" @click="active = 1">{{ $t('pageSign.login_pwd') }}</span>
          <span :class="{ active: active === 2 }" @click="active = 2">{{ $t('pageSign.login_code') }}</span>
        </div>
        <van-form v-if="active === 1" label-width="4em" @submit="onSubmit">
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
            v-model="password"
            type="password"
            :label="$t('pageSign.pwd')"
            :placeholder="$t('pageSign.pwd')"
            :rules="[{ required: true }]"
          />
          <van-button block type="info" native-type="submit" class="submit">{{ $t('login') }}</van-button>
        </van-form>
        <van-form v-else label-width="4em" @submit="onSubmit">
          <van-field
            v-model="username"
            :label="$t('pageSign.phone')"
            :rules="[{ required: true }]"
          >
            <div slot="input" class="slot-inp">
              <span class="tel-area" @click="showPicker=true">{{ area_num }} -</span>
              <input
                v-model="username"
                type="text"
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
            <template v-if="active === 2" #button>
              <van-button
                size="small"
                type="primary"
                block
                :disabled="times !== 60"
                @click.prevent="handleGetCode"
              >
                <template v-if="times === 60">{{ $t('pageSign.send_code') }}</template>
                <template v-else>{{ times }}s</template>
              </van-button>
            </template>
          </van-field>
          <van-button block type="info" native-type="submit" class="submit"> {{ $t('login') }} </van-button>
        </van-form>
        <div class="links">
          <nuxt-link to="/sign/register">{{ $t('pageSign.free_reg') }}</nuxt-link>
          <div class="divider"></div>
          <nuxt-link to="/sign/forget">{{ $t('pageSign.forget_pwd') }}</nuxt-link>
        </div>
      </div>
    </div>
    <van-popup v-model="showPicker" position="bottom" round>
      <van-picker show-toolbar :columns="areaNums" :visible-item-count="10" @confirm="confirmArea" @cancel="showPicker=false" />
    </van-popup>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
import { areaNums } from '@/constants/area_nums'
export default {
  data () {
    return {
      areaNums,
      logo: require('@/assets/images/login_logo.png'),
      active: 1,
      username: '',
      password: '',
      verification_code: '',
      times: 60,
      loginType: 'phone',
      area_num: '86',
      showPicker: false
    }
  },
  methods: {
    ...mapActions({
      getCode: 'user/getCode',
      login: 'user/login'
    }),
    handleGetCode () {
      const username = this.loginType === 'phone' ? `${this.area_num}-${this.username}` : this.username
      this.$toast.loading()
      this.getCode(username)
        .then(({ msg }) => {
          this.$toast(msg)
          this.getTime()
        })
        .catch(({ msg }) => {
          this.$toast(msg)
        })
    },
    onSubmit () {
      this.$toast.loading()
      const username = this.loginType === 'phone' ? `${this.area_num}-${this.username}` : this.username
      const payload = { username, device_type: 'web' }
      if (this.active === 1) {
        payload.password = this.password
      } else {
        payload.verification_code = this.verification_code
      }
      this.$toast.loading()
      this.login([this.active, payload])
        .then((res) => {
          this.$toast(res.msg)
          this.$nextTick(() => {
            this.$router.replace('/home')
          })
        })
        .catch((res) => {
          this.$toast(res.msg)
        })
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
    confirmArea (values) {
      this.area_num = values.phone_code
      this.showPicker = false
    }
  }
}
</script>

<style scoped lang="less">
.container {
  height: 100vh;
  background: linear-gradient(135deg, @themeColor 0 50%, #fff 50% 100%);
}
.card {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  transform: translateY(-8%);
}
.card-shadow {
  width: 90vw;
  padding: 10vw 5vw;
  border-radius: 10px;
  background-color: rgba(255, 255, 255, 0.8);
  -webkit-backdrop-filter: blur(10px);
  backdrop-filter: blur(10px);
  box-shadow: 10px 10px 50px -20px rgba(0, 0, 0, 0.4);
  border-top: 1px solid rgba(255, 255, 255, 0.5);
  border-left: 1px solid rgba(255, 255, 255, 0.5);
  border-right: 1px solid rgba(255, 255, 255, 0.2);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}
.form-title {
  color: #ffffff;
  margin-bottom: 30px;
  font-weight: 500;
  text-align: center;
}
/deep/ .van-field {
  border-radius: 10px;
  margin-bottom: 15px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}
.submit {
  border-radius: 10px;
  margin-bottom: 25px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}
.divider {
  display: inline-block;
  vertical-align: middle;
  width: 1px;
  height: 16px;
  margin: 0 10px;
  background-color: #eee;
  transform: scaleX(0.5);
}
.links {
  text-align: center;
  a {
    color: @themeColor;
  }
}
.tab {
  margin-bottom: 30px;
  color: #333;
  display: flex;
  text-align: center;
  justify-content: space-around;
  align-items: center;
  font-size: 16px;
  font-weight: 500;
  span {
    cursor: pointer;
    transition: 0.3s;
    &::after {
      content: '';
      position: absolute;
      top: 120%;
      left: 50%;
      width: 20px;
      height: 2px;
      margin-left: -10px;
      transition: 0.3s;
    }
  }
  .active {
    position: relative;
    transform: scale(1.2);
    &::after {
      background-color: @themeColor;
    }
  }
}
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
