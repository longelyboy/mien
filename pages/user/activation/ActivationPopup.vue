<template>
  <van-dialog
    v-model="showCodePop"
    :title="$t('title')"
    :confirm-button-text="$t('get')"
    show-cancel-button
    @confirm="onActive"
  >
    <van-cell-group>
      <van-field
        v-model="activationCode"
        :label="$t('key')"
        label-width="4em"
        :placeholder="$t('please')"
      />
    </van-cell-group>
  </van-dialog>
</template>

<script>
import { mapActions } from 'vuex'
export default {
  i18n: {
    messages: {
      zh: {
        title: '输入激活码',
        get: '领取',
        key: '激活码',
        please: '请输入激活码'
      },
      en: {
        title: 'Enter the CD-Key',
        get: 'Get it',
        key: 'CD-Key',
        please: 'Please enter the CD-Key'
      }
    }
  },
  data () {
    return {
      showCodePop: false,
      activationCode: ''
    }
  },
  methods: {
    ...mapActions({
      cdkeyActive: 'user/cdkeyActive'
    }),
    onActive () {
      this.$dialog
        .confirm({
          title: '提示',
          message: `领取该激活码? \n ${this.activationCode}`
        })
        .then(() => {
          this.$toast.loading()
          this.cdkeyActive({ keys: this.activationCode }).then(({ msg }) => {
            this.$toast(msg)
            // this.$toast(res.msg)
          })
            .catch(({ msg }) => {
              this.$toast(msg)
            })
        })
    }
  }
}
</script>

<style>

</style>
