<template>
  <div>
    <van-nav-bar
      title="我的跟单"
      left-arrow
      @click-left="$router.back()"
    />
    <div class="my-info">
      <van-row class="hd" type="flex" justify="space-between" aling="center">
        <van-col style="font-size: 1.2em">我的跟单</van-col>
        <van-col>计价单位：USDT</van-col>
      </van-row>
      <van-row class="bd" type="flex">
        <van-col span="9">
          <div class="label van-ellipsis">跟单总金额</div>
          <div class="van-ellipsis">0.00</div>
        </van-col>
        <van-col span="9">
          <div class="label van-ellipsis">收益额</div>
          <div class="van-ellipsis">0.00</div>
        </van-col>
        <van-col class="right" span="6">
          <div class="label van-ellipsis">收益率</div>
          <div class="van-ellipsis">+0%</div>
        </van-col>
      </van-row>
    </div>
    <van-tabs v-model="active">
      <van-tab title="进行中">内容 1</van-tab>
      <van-tab title="已结束">内容 2</van-tab>
      <van-tab title="我的跟单">内容 3</van-tab>
    </van-tabs>
  </div>
</template>

<script>
export default {
  data () {
    return {
      active: '1'
    }
  }
}
</script>

<style lang="less" scoped>
.my-info {
  background-color: #fff;
  margin-bottom: 10px;
  .hd {
    padding: 10px 15px;
  }
  .bd {
    font-size: 12px;
    .van-col {
      padding: 0 15px;
      margin-bottom: 15px;
    }
    .label {
      font-size: .8em;
      color: #888;
      margin-bottom: 5px;
    }
    .right {
      text-align: right;
    }
  }
}
</style>
