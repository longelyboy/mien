<template>
  <div>
    <van-nav-bar
      :title="$t(platforms[active].label)"
      left-arrow
      @click-left="$router.back()"
    />
    <van-form @submit="onSubmit">
      <van-field
        v-model="api_key"
        label="Api Key"
        placeholder="Api Key"
        :rules="[{ required: true }]"
      />
      <van-field
        v-model="secret_key"
        label="Secret Key"
        placeholder="Secret Key"
        :rules="[{ required: true }]"
      />
      <van-field
        v-if="platform === 'okex'"
        v-model="passphrase"
        label="Passphrase"
        placeholder="Passphrase"
        :rules="[{ required: true }]"
      />
      <div style="margin: 16px">
        <van-button
          round
          block
          type="info"
          native-type="submit"
        >
          {{ $t('actions.import') }}
        </van-button>
      </div>
    </van-form>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
export default {
  data () {
    return {
      api_key: '',
      secret_key: '',
      passphrase: ''
    }
  },
  computed: {
    ...mapState({
      platforms: ({ authorize }) => authorize.platform
    }),
    active () {
      return this.$route.query.active
    },
    platform () {
      const p = this.platforms[this.active]
      this.api_key = p.api_key
      this.secret_key = p.secret_key
      this.passphrase = p.passphrase
      return p.label
    }
  },
  methods: {
    ...mapActions({
      editApiAccount: 'authorize/editApiAccount'
    }),
    onSubmit () {
      const payload = {
        platform: this.platform,
        api_key: this.api_key,
        secret_key: this.secret_key,
        passphrase: this.platform === 'okex' ? this.passphrase : '-'
      }
      this.$toast.loading()
      this.editApiAccount(payload).then((res) => {
        this.$toast(res.msg)
        this.$router.back()
      }).catch(({ msg }) => {
        this.$toast(msg)
      })
    }
  }
}
</script>

<style scoped lang="less">
.van-cell {
  display: block;
}
</style>
