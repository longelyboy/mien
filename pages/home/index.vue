<template>
  <div class="conten">
    <div class="topimg" >
      <!-- <img src="../../assets/images/homelogo.png" alt=""> -->
    </div>
    <van-swipe class="my-swipe" :autoplay="3000" indicator-color="white">
      <van-swipe-item v-for="item in banner.list" :key="item.id">
        <van-image style="width: 100%;
  height: 150px;" height="46vw" fit="cover" :src="item.image" @click="viewDetail(item)"
        />
      </van-swipe-item>
    </van-swipe>
    <notice></notice>
    <rank></rank>
    <ul>
      <li @click="handleLink('https://accounts.binance.com/zh-CN/register?ref=108187771')">
        <p>币安注册 <img src="../../assets/images/binance.png" alt=""> </p>
        <span>震荡行情，高抛低吸，稳定获利</span>
      </li>
      <li @click="handleLink('https://www.okexa.com/join/11800910')">
        <p>OKEX注册 <img src="../../assets/images/okex.png" alt=""> </p>
        <span>智能追踪，让买入成本更低，卖出盈利更对</span>
      </li>
    </ul>
    <menu-pic></menu-pic>
    <markets></markets>
    <div v-show="show" class="van-overlay" @click="show=false">
      <p>{{ $t('msg.Stay_tuned') }}<!-- 敬请期待 --></p>
    </div>
  </div>
</template>

<script>
import { Swipe, SwipeItem, Dialog } from 'vant'
import { mapState, mapActions } from 'vuex'
import notice from './components/notice'
import rank from './components/rank'
import menuPic from './components/menuPic'
import markets from './components/markets'

export default {
  layout: 'navigation',
  components: {
    [Swipe.name]: Swipe,
    [SwipeItem.name]: SwipeItem,
    notice,
    rank,
    menuPic,
    markets
  },
  data() {
    return { show: false }
  },
  computed: {
    ...mapState({
      banner: index => index.banner
    })
  },
  mounted() {
    this.getBanner()
  },
  methods: {

    ...mapActions({
      getBanner: 'getBanner'
    }),
    
     handleLink (path) {
      window.open(path)
    },
    viewDetail(item) {
      this.$router.push({
        name: 'common-article',
        params: {
          url: item.url,
          title: item.title
        }
      })
    }
  }
}
</script>

<style scoped lang="less">
.van-overlay{
  z-index: 11111;
  background: none;
 p{
    background-color: rgba(0, 0, 0, 0.7);
    width:334px;
    line-height:60px;
    height: 60px;
    z-index: 1111;
    color: #fff;
    text-align: center;
    margin:auto;
    margin-top: 34vh;

    border-radius: 10px;
 }
}
.conten{
  padding: 10px 10px 0;
  background: #fff;
}

.topimg{
  width: 100%;
  text-align: center;
  margin: 20px 0 18px;
  img{
    width: 107px;
  }
}
.my-swipe {
  height: 150px;
}
.van-swipe-item {
  font-size: 0;
}
h4{
  color: #333333;
  font-size: 18px;
}
ul{
  width: 100%;
  overflow: hidden;
  margin-top: 10px;
  li{
    width: 48%;
    height: 82px;
    background: #F1F2F9;
    float: left;
    padding: 10px;
    box-sizing: border-box;
    margin-bottom: 10px;
    p{
      color: #2E3233;
      font-size:16px;
      font-weight: 700;
      overflow: hidden;
      margin-bottom: 8px;
      img{
        float: right;
        width: 22px;
      }
    }
    span{
      color: #909399;
      font-size: 12px;
    }
  }
  li:nth-child(odd){
    float: right;
  }
}
</style>
