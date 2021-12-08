<template>
  <div>
    <van-nav-bar :title="$t('title')" left-arrow @click-left="$router.back()" />
    <van-cell-group>
      <van-uploader :after-read="afterRead">
        <van-cell :title="$t('head')" is-link>
          <template>
            <van-image class="header" :src="userInfo.avatar" />
          </template>
        </van-cell>
      </van-uploader>
      <van-cell :title="$t('nick')" :value="userInfo.user_nickname" is-link @click="showNickPop = true" />
      <van-cell :title="$t('signature')" :value="userInfo.signature" is-link @click="showSignPop = true" />
    </van-cell-group>
    <van-dialog
      v-model="showNickPop"
      :title="$t('edit_nick')"
      show-cancel-button
      @confirm="handleSave('user_nickname')"
    >
      <van-cell-group>
        <van-field v-model="user_nickname" input-align="center" :placeholder="$t('please')" />
      </van-cell-group>
    </van-dialog>
    <van-dialog
      v-model="showSignPop"
      :title="$t('edit_sign')"
      show-cancel-button
      @confirm="handleSave('signature')"
    >
      <van-cell-group>
        <van-field
          v-model="signature"
          rows="2"
          type="textarea"
          maxlength="20"
          show-word-limit
        />
      </van-cell-group>
    </van-dialog>
  </div>
</template>

<script>
import { Uploader } from 'vant'
import { mapState, mapActions } from 'vuex'

export default {
  i18n: {
    messages: {
      zh: {
        title: '个人资料',
        head: '头像',
        nick: '昵称',
        signature: '个人签名',
        edit_nick: '编辑昵称',
        please: '请输入昵称',
        edit_sign: '编辑个人签名'
      },
      en: {
        title: 'Personal Information',
        head: 'Avatar',
        nick: 'Nickname',
        signature: 'Signatures',
        edit_nick: 'Edit nickname',
        please: 'Please enter a nickname',
        edit_sign: 'Edit personal signature'
      }
    }
  },
  components: {
    [Uploader.name]: Uploader
  },
  data () {
    return {
      avatar: require('@/assets/images/header.png'),
      user_nickname: '',
      signature: '',
      showNickPop: false,
      showSignPop: false
    }
  },
  computed: {
    ...mapState({
      userInfo ({ user }) {
        const info = user.userInfo
        this.user_nickname = info.user_nickname
        this.signature = info.signature
        return info
      }
    })
  },
  watch: {
    userInfo (value) {
      this.user_nickname = value.user_nickname
      this.signature = value.signature
    }
  },
  methods: {
    ...mapActions({
      upload: 'upload',
      editUserInfo: 'user/editUserInfo',
      getUserInfo: 'user/getUserInfo'
    }),
    afterRead (file) {
      const toast = this.$toast.loading()
      this.upload(file.file).then((res) => {
        this.avatar = res.data.url
        this.$nextTick(() => {
          this.handleSave('avatar')
        })
      }).finally(() => {
        toast.clear()
      })
    },
    handleSave (name) {
      const toast = this.$toast.loading()
      this.editUserInfo({ [name]: this[name] }).then((res) => {
        this.$toast(res.msg)
        this.getUserInfo()
      }).finally(() => {
        toast.clear()
      })
    }
  }
}
</script>

<style scoped lang="less">
.header {
  float: right;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  overflow: hidden;
}
/deep/ .van-dialog__content {
  padding: 30px 15px;
}
/deep/ .van-uploader {
  display: block;
  .van-uploader__input-wrapper {
    flex: 1;
  }
}
/deep/ .van-cell__title {
  width: 5em;
  flex: 0 0 auto;
}
</style>
