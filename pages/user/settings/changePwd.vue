<template>
  <div>
    <van-nav-bar
      :title="$t('title')"
      left-arrow
      @click-left="$router.back()"
    />
    <van-form
      label-width="9em"
      @submit="onSubmit"
    >
      <van-field
        v-model="old_password"
        type="password"
        :label="$t('old')"
        :placeholder="`${$t('please')}${$t('old')}`"
        :rules="[{ required: true, message: `${$t('please')}${$t('old')}` }]"
      />
      <van-field
        v-model="password"
        type="password"
        :label="$t('new')"
        :placeholder="`${$t('please')}${$t('new')}`"
        :rules="[{ required: true, message: `${$t('please')}${$t('new')}` }]"
      />
      <van-field
        v-model="confirm_password"
        type="password"
        :label="$t('confirm')"
        :placeholder="`${$t('please')}${$t('confirm')}`"
        :rules="[{ required: true, message: `${$t('please')}${$t('confirm')}` }]"
      />
      <div style="margin: 15px">
        <van-button
          block
          type="info"
          native-type="submit"
          class="submit"
        >
          {{ $t('actions.submit') }}
        </van-button>
      </div>
    </van-form>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
export default {
  i18n: {
    messages: {
      zh: {
        title: '修改密码',
        old: '旧密码',
        new: '新密码',
        confirm: '确认密码',
        please: '请填写'
      },
      en: {
        title: 'Change password',
        old: 'Old Password',
        new: 'New Password',
        confirm: 'Confirm Password',
        please: 'Please fill in '
      },
      hk: {
        title: '修改密碼',
        old: '舊密碼',
        new: '新密碼',
        confirm: '確認密碼',
        please: '請填寫'
      }
    }
  },
  data () {
    return {
      old_password: '',
      password: '',
      confirm_password: ''
    }
  },
  methods: {
    ...mapActions({
      changePwd: 'user/changePwd'
    }),
    onSubmit () {
      this.changePwd({
        old_password: this.old_password,
        password: this.password,
        confirm_password: this.confirm_password
      }).then((res) => {
        this.$toast(res.msg)
        this.$router.back()
      })
    }
  }
}
</script>

<style scoped lang="less">
</style>
