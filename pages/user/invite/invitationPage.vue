<template>
  <div class="invitationPage">
    <div class="conter">
      <p class="imger"><img src="../../../assets/images/logo.png" alt=""></p>
      <p>邀你一起参与MIEN交易所</p>
    </div>
    <div class="bottom">
      <div class="logo">
        <img src="../../../assets/images/InvitationPageLogo.png" alt="">
      </div>
      <div class="bottom_conter">
        <p>注册即可交易</p>
        <p class="text">长按识别二维码 邀请您加入MIEN</p>
      </div>
      <div class="qrCodeDom">
        <div id="code" class="code"></div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import QRCode from 'qrcodejs2'
export default {
  name: 'InvitationPage',
  data () {
    return {
      code: '',
      showCode: false,
    }
  },
  computed: {
    ...mapState({
      userInfo: ({ user }) => user.userInfo
    })
  },
  created () {
    this.getCode()
  },
  methods: {
    getCode () {
      this.$nextTick(() => {
        this.code = new QRCode('code', {
          width: 66,
          height: 66,
          text: this.userInfo.invitation_url,
        })
      })
    }
  },
}
</script>

<style lang="less">
.invitationPage{
  .conter{
    width: 100%;
    height: calc(100vh - 88px);
    background: url('../../../assets/images/InvitationPage.png') no-repeat;
    background-size: 100% 100%;
    padding-top: 58px;
    p{
      color: #fff;
      font-size: 24px;
      font-weight: 500;
      text-align: center;
    }
    .imger{
      width: 111px;
      height: 111px;
      border: 1px solid #fff;
      border-radius: 50%;
      margin: 0 auto 18px;
      display: flex;
      justify-content: center;
      align-items: center;
      img{
        width: 96px;
        height: 96px;
      }
    }
  }
  .bottom{
    height: 88px;
    background-color: #fff;
    padding: 15px;
    display: flex;
    align-items: center;
    .logo{
      margin-right: 9px;
      img{
        width: 59px;
        height: 59px;
      }
    }
    .bottom_conter{
      color: #333;
      font-size: 15px;
      margin-right: 19px;
      .text{
        color: #666;
        font-size: 12px;
      }
    }
    .qrCodeDom{
      width: 66px;
      height: 66px;
      text-align: center;
      line-height: 66px;
      color: #fff;
      #qrcode{
        height: 66px;
      }
    }
  }
}
</style>
