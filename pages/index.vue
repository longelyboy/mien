<template>
  <nuxt />
</template>

<script>
import { mapActions } from 'vuex'
export default {
  data () {
    return {
      authToken: this.$route.query.token
    }
  },
  created () {
    this.needAuth()
  },
  methods: {
    ...mapActions({
      openAuthLogin: 'user/openAuthLogin',
      getUserInfo: 'user/getUserInfo'
    }),
    needAuth () {
      if (this.authToken) {
        this.$toast.loading('身份验证中...')
        this.openAuthLogin({ token: this.authToken })
          .then(() => {
            this.getUserInfo()
            this.$toast('授权登录成功')
            this.$router.push('/home')
          })
          .catch(({ msg }) => {
            this.$toast(msg)
          })
      } else {
        this.$router.push('/home')
      }
    }
  }
}
</script>
