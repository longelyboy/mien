<template>
  <div class="top1">
    <van-nav-bar fixed placeholder left-arrow title="抽奖" @click-left="$router.back()" />
    <div class="zp_box">
      <LuckyWheel
        ref="LuckyWheel"
        width="300px"
        height="300px"
        :prizes="prizes"
        :default-style="defaultStyle"
        :blocks="blocks"
        :buttons="buttons"
        @start="startCallBack"
        @end="endCallBack"
      />
    </div>

    <div class="list">
      <p>
        <span>中奖榜单</span>
        <!-- <i>我的中奖记录>></i> -->
      </p>
      <ul>
        <li>手机号</li>
        <li>奖励(元)</li>
      </ul>
      <ul v-for="(item) in list" :key="item.id" class="list">
        <li>{{ item.mobile }}</li>
        <li><span>{{ item.amount }}</span></li>
      </ul>
    </div>
  </div>
</template>
<script>
import { mapState, mapActions } from 'vuex'

export default {
  layout: 'navigation',
  i18n: {
    messages: {
      zh: {
        contact: '联系我们',
        language: '选择语言',
        tip1: '您的vip身份到期时间为',
        tip2: '您的vip身份已到期！'
      },
      en: {
        contact: 'Contact Us',
        language: 'Change Language',
        tip1: 'Your VIP status expires at',
        tip2: 'Your vip status has expired!'
      }
    }
  },
  components: {
  },
  data () {
    return {
      prizes: [],
      defaultStyle: {
        fontColor: '#d64737',
        fontSize: '14px'
      },
      list: [],
      blocks: [
        { padding: '13px', background: '#ffc324' }
        // { imgs: [{ src: require('../../../assets/images/bj1.png'), width: '10%', top: '-100%' }] }

      ],
      buttons: [
        { radius: '50px', background: '#fcbd67' },
        { radius: '60px', background: '#fcbd67' },
        { radius: '41px', background: '#e74e41', pointer: true },
        {
          radius: '50px',
          background: '#e74e41',
          imgs: [{ src: require('../../../assets/images/bj4.png'), width: '100%', top: '-100%' }]
        }
      ]
    }
  },
  computed: {
    ...mapState({
      locale: state => state.locale
    })
  },
  mounted () {
    this.getPrizesList()
  },
  created() {
    this.GetGamelogList()
  },
  methods: {
    ...mapActions({
      accountGame: 'wallet/accountGame',
      GamelogList: 'wallet/GamelogList'
    }),
    GetGamelogList() {
      this.GamelogList({})
        .then((res) => {
          this.list = res.data.list
          console.log(this.list)
        })
        .catch((res) => {
          console.log(res)
        })
    },
    getPrizesList () {
      const prizes = []
      const data = ['一等奖', '未中奖', '二等奖', '未中奖', '三等奖', '未中奖', '四等奖', '未中奖']
      data.forEach((item, index) => {
        prizes.push({
          title: item,
          background: index % 2 ? '#fff3ae' : '#fefcd7',
          fonts: [{ text: item, top: '10%' }],
          imgs: [{ src: require('../../../assets/images/hongbao.png'), width: '30%', top: '35%' }]
        })
      })
      this.prizes = prizes
    },
    startCallBack () {
      const _this = this
      _this.$refs.LuckyWheel.play()

      _this.accountGame({})
        .then((res) => {
          if (res.code === 1) {
            _this.$refs.LuckyWheel.stop(res.data >> 0)
            // _this.$refs.LuckyWheel.stop(Math.random() * 8 >> 0)
            // _this.$refs.luckyWheel.stop(1 >> 0)
          // _this.$toast(res.msg)
          }
        })
        .catch((res) => {
          // _this.$refs.luckyWheel.stop(1 >> 0)
          _this.$toast(res.msg)
        })
    },
    // startCallBack2 () {
    //   this.$refs.LuckyWheel.play()
    //   setTimeout(() => {
    //     this.$refs.LuckyWheel.stop(1 * 8 >> 0)
    //   }, 3000)
    // },
    endCallBack (prize) {
      if (prize.title === '未中奖') {
        this.$toast('未中奖')
      } else {
        this.$toast(`恭喜你获得${prize.title}`)
      }
    }
  }
}
</script>

<style scoped lang="less">

.top1{
  background-image: url('../../../assets/images/bj.png');
  background-size: 100%;
  height: 100%;
  background-position: center 67px;
  padding-bottom: 30px;
  .zp_box{
    width: 329px;
    margin: auto;
    margin-top: 160px;
    box-sizing: border-box;
    // background-image: url(/_nuxt/assets/images/bj1.png);
    background-size: 100% 100%;
    overflow: hidden;
    >div{
      margin-top: 22px;
      margin-left: 15px;
    }
  }
}
.list{
  background:#FFFEF0;
  width: 347px;
  margin: auto;
  margin-top: 20px;
  border-radius: 8px;
    overflow: hidden;
  p:first-child{
    padding: 10px 10px 30px 10px;
    box-sizing: border-box;
    border-bottom: 1px solid #C0C0C0;
    span{
      float: left;
      font-style: 14px;
      font-weight: 700;
      color: #333333;
    }
    i{
      float: right;
      font-style: 12px;
      color: #2582FC;
      font-style: normal;
    }

  }
  ul{
    padding: 0 10px;
    box-sizing: border-box;
    color: #9AA3A9;
    li{
      padding: 0 6px;
      box-sizing: border-box;
      font-size: 14px;
      float: left;
      line-height: 56px;
      width: 50%;
    }
    // li:first-child,li:nth-child(3){
    //   width: 100px;
    // }
    li:nth-child(1){
      // width: calc(100% - 200px);
      text-align: left;
    }
    li:nth-child(2){
      text-align: right;
    }
  }
  ul.list{
    padding: 0 10px;
    box-sizing: border-box;
    color: #9AA3A9;
    li{
      padding: 0 6px;
      box-sizing: border-box;
      font-size: 14px;
      float: left;
      line-height: 56px;
      width: 50%;
    }
    // li:first-child,li:nth-child(3){
    //   width: 100px;
    // }
    li:nth-child(1){
      // width: calc(100% - 200px);
      text-align: left;
    }
    li:nth-child(2){
      text-align: right;
      span{
          background: #fef6d9;
          color: #FE8A00;
          width: 60px;
          line-height: 25px;
          display: inline-block;
          text-align: center;
          font-weight: 700;
      }
    }
  }
}
</style>
