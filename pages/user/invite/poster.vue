<template>
  <div class="Poster">
    <van-nav-bar :title="$t('title')" left-arrow @click-left="$router.back()" />
    <div class="conter">
      <div class="top">
        <p>好友: 0</p>
        <p><img src="../../../assets/images/logo.png" alt=""></p>
      </div>
      <div class="Invitation">
        <p class="h3">邀请中心</p>
        <p class="p1">邀请好友，享更多权益</p>
      </div>
      <div v-for="(item,index) in posterList" :key="index" class="posterList" >
        <div class="h4">
          <p>{{ item.title }}</p>
          <p class="bluePrice">仅售{{ item.price }}USDT</p>
        </div>
        <p class="describe">{{ item.describe }}</p>
        <p class="blueBuy">立即购买<span><img src="../../../assets/images/BlueNext.png" alt=""></span></p>
      </div>
    </div>
    <div class="copy">
      <div class="copyDiv">
        <p>邀请码: <span>{{ code }}</span>  <img src="../../../assets/images/copy.png" alt=""></p>
        <div class="btn">
          <div v-clipboard:success="onCopy" v-clipboard:copy="code" class="btnWhite">复制邀请链接</div>
          <div class="btnBlue" @click="goInvitationPage">生成邀请海报</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Poster',
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
      posterList: [
        {
          title: '高级用户',
          price: '1000.00',
          describe: '活动期间，升级成为高级用户，赠送等值1000智点。邀请用户升级或充值，获20%奖励，自用省钱，分享赚钱。'
        },
        {
          title: 'VIP用户',
          price: '5000.00',
          describe: '活动期间，升级成为VIP用户，赠送等值5000智点。邀请用户升级或充值，获40%奖励，自用省钱，分享赚钱。'
        }
      ]
    }
  },
  methods: {
    onCopy () {
      this.$toast('复制成功')
    },
    goInvitationPage () {
      this.$router.push({ path: '/user/invite/invitationPage' })
    }
  }
}
</script>

<style lang="less">
.Poster{
  .conter{
    margin-top: 10px;
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
    .Invitation{
        margin: 12px 0 26px;
        height: 95px;
        padding: 16px 23px;
        background: url('../../../assets/images/Invitation.png') no-repeat;
        background-size: 100%;
        color: #fff;
        .h3{
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 10px;
        }
        .p1{
            color:#DDEAFF;
            font-size: 12px;
        }
    }
    .posterList{
      height: 152px;
      padding: 14px;
      border: 1px #DDDDDD solid;
      border-radius: 10px;
      margin-bottom: 14px;
      font-size: 14px;
      font-weight: 600;
      .h4{
          display: flex;
          justify-content: space-between;
          color: #000;
          .bluePrice{
              color: #2C77E8;
          }
      }
      .describe{
          font-weight: 400;
          color: #999;
          margin: 14px 0 8px;
      }
      .blueBuy{
          color: #2C77E8;
          text-align: right;
      }
      img{
          width: 16px;
          height: 16px;
          vertical-align: middle;
      }
    }
  }
  .copy{
        padding-top: 14px;
        padding-bottom: 20px;
        border-top: 1px solid #DDDDDD;
        background-color: #fff;
        .copyDiv{
            padding: 0 14px;
            p{
                span{
                    color: #2C77E8;
                }
            }
            img{
                width: 20px;
                height: 20px;
                vertical-align: middle;
            }
            .btn{
                margin-top: 11px;
                display: flex;
                div{
                  border-radius: 5px;
                  width: 167px;
                  height: 44px;
                  text-align: center;
                  line-height: 44px;
                }
                .btnWhite{
                  border: 1px solid #2C77E8;
                  color: #2C77E8;
                  margin-right: 14px;
                }
                .btnBlue{
                  color: #fff;
                  background-color: #2C77E8;
                }
            }
        }
    }
}
</style>
