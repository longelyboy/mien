<template>
  <div>
    <van-nav-bar :title="$t('title')" left-arrow @click-left="$router.back()" />
    <div class="share-box">
      <div class="bg">
        <img src="@/assets/images/share-title.png" alt="" class="share-title">
        <div class="col">
          <div class="code">{{ userInfo.invitation_code || 'IAFAED' }}</div>
          <van-button v-clipboard:copy="userInfo.invitation_code" v-clipboard:success="onCopy" color="#595fe7" type="primary" size="small" class="btn">{{ $t('invitation_code') }}</van-button>
        </div>
        <div class="col">
          <div id="qrcode" ref="qrCodeUrl" class="qr"></div>
        </div>
        <div class="share-ft">
          <span>扫码下载我们的APP</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import QRCode from 'qrcodejs2'
import { posterShare } from '@/utils/jsbridge'
let timer = null
export default {
  i18n: {
    messages: {
      zh: {
        title: '邀请注册',
        invitation_code: '点击复制邀请码'
      },
      en: {
        title: 'Invitation to register',
        invitation_code: 'Invitation Code'
      }
    }
  },
  computed: {
    ...mapState({
      userInfo: ({ user }) => user.userInfo
    })
  },
  mounted () {
    new QRCode(this.$refs.qrCodeUrl, {
      text: this.userInfo.invitation_url,
      width: 140,
      height: 140
    })

    timer = setTimeout(() => {
      posterShare()
    }, 2000)
    this.$once('hook:destroyed', () => {
      clearTimeout(timer)
      timer = null
    })
  },
  methods: {
    onCopy () {
      this.$toast('复制成功')
    }
  }
}
</script>

<style lang="less" scoped>
.share-box {
  position: relative;
  background: no-repeat center top;
  background: linear-gradient(180deg, #141935, #6267ff);
  height: calc(100vh - 46px);
  background-size: 100% auto;
  padding: 5%;
  .bg {
    position: relative;
    height: 100%;
    background: #fff;
    background:
      radial-gradient(circle at 0 45%, transparent 12px, #fff 0),
      radial-gradient(circle at 100% 45%, transparent 12px, #fff 0);
    background-size: 51% 100%, 51% 100%;
    background-repeat: no-repeat;
    background-position: 0 0,100% 0;
    box-shadow: 5px 5px 30px -5px rgba(0, 0, 0, .1);
    overflow: hidden;
    &::after {
      content: '';
      position: absolute;
      left: 12px;top: 45%;
      height: 0;
      width: calc(100% - 24px);
      border-bottom: 1px dashed #eee;
    }
  }
  .col {
    height: 45%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
  .code {
    color: #595fe7;
    font-weight: 500;
    font-size: 2em;
    margin-bottom: 10px;
  }
  .qr {
    padding: 10px;
    border-radius: 5px;
    background-color: #fff;
    box-shadow: 0 0 20px -5px rgba(0, 0, 0, 0.3);
  }
}
.share-title {
  position: absolute;
  top: 5%;
  left: 10%;
  width: 80%;
}
.share-ft {
  position: absolute;
  bottom: 5%;
  left: 10%;
  width: 80%;
  text-align: center;
  color: #888;
  &::before {
    content: '';
    position: absolute;
    top: 50%;left: 0;
    width: 100%;
    height: 0;
    border-bottom: 1px solid #eee;
  }
  span {
    position: relative;
    display: inline-block;
    background-color: #fff;
    padding: 0 20px;
  }
}
</style>
