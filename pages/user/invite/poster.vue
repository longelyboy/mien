<template>
  <div class="Poster">
    <van-nav-bar :title="$t('title')" fixed left-arrow @click-left="$router.back()" />
    <div class="conter">
      <div class="top">
        <p>好友: {{ invite_count }}</p>
        <p><img src="../../../assets/images/logo.png" alt=""></p>
      </div>
      <div class="Invitation">
        <p class="h3">邀请中心</p>
        <p class="p1">邀请好友，享更多权益</p>
      </div>
      <div v-for="(item,index) in posterList" :key="index" class="posterList" >
        <div class="h4">
          <p>{{ item.level_name }}</p>
          <p class="bluePrice">仅售{{ item.need_recharge_num }}USDT</p>
        </div>
        <p class="describe">{{ item.remark }}</p>
        <p class="blueBuy" @click="goReceive">立即购买<span><img src="../../../assets/images/BlueNext.png" alt=""></span></p>
      </div>
    </div>
    <div class="copy">
      <div class="copyDiv">
        <p>邀请码: <span>{{ userInfo.invitation_code }}</span>  <img v-clipboard:success="onCopy" v-clipboard:copy="userInfo.invitation_code" src="../../../assets/images/copy.png" alt=""></p>
        <div class="btn">
          <div v-clipboard:success="onCopy" v-clipboard:copy="userInfo.invitation_url" class="btnWhite">复制邀请链接</div>
          <div class="btnBlue" @click="goInvitationPage">生成邀请海报</div>
        </div>
        <div class="share-ft">
          <span>扫码下载我们的APP</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
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
  data () {
    return {
      code: '123',
      invite_count: '',
      posterList: [
        {
          level_name: '高级用户',
          need_recharge_num: '1000.00',
          remark: '活动期间，升级成为高级用户，赠送等值1000智点。邀请用户升级或充值，获20%奖励，自用省钱，分享赚钱。'
        },
        {
          level_name: 'VIP用户',
          need_recharge_num: '5000.00',
          remark: '活动期间，升级成为VIP用户，赠送等值5000智点。邀请用户升级或充值，获40%奖励，自用省钱，分享赚钱。'
        }
      ]
    }
  },
  computed: {
    ...mapState({
      userInfo: ({ user }) => user.userInfo
    })
  },
  created () {
    this.getinvitationLevelList().then(({ data: { list, data }}) => {
      this.invite_count = data
      this.posterList = list
    }).catch((err) => {
      console.log(err)
    })
  },
  methods: {
    ...mapActions({
      getinvitationLevelList: 'user/getinvitationLevelList'
    }),
    goReceive () {
      this.$router.push({ path: '/wallet/receive', query: { symbol: 'USDT-TRC' }})
    },
    onCopy () {
      this.$toast('复制成功')
    }
  }
}
</script>

<style lang="less">
.Poster{
  .van-nav-bar{
    margin: 0;
    padding-top: 20px;
  }
  .conter{
    margin-top: 76px;
    padding: 0 14px 20px;
    background-color: #fff;
    .top{
        padding-top: 7px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        img{
            width: 84px;
            height: 84px;
        }
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
