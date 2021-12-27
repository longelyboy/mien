<template>

  
  <van-row class="nav-pic" type="flex" gutter="15">

    
    <van-col style="width:48%;float:left;margin-right:10px;padding-right:0;">
      <nuxt-link to="/authorize" class="nav-item" :style="{ 'background-image': `url(${image1})` }">
        <p class="title">{{ $t('homeMenu.item1.title') }}</p>
        <p class="sub">{{ $t('homeMenu.item1.sub') }}</p>
      </nuxt-link>
    </van-col>
    <van-col style="width:48%;float:left;padding-left:0;">
      <nuxt-link to="/home/revenue" class="nav-item" :style="{ 'background-image': `url(${image2})` }">
        <p class="title">{{ $t('homeMenu.item2.title') }}</p>
        <p class="sub">{{ $t('homeMenu.item2.sub') }}</p>
      </nuxt-link>
    </van-col>
  </van-row>
</template>

<script>
export default {
  data () {
    return {
      image1: require('@/assets/images/image1.png'),
      image2: require('@/assets/images/image2.png')
    }
  }
}
</script>

<style scoped lang="less">
.nav-pic {
  background-color:#F1F2F9;
  margin-bottom: 10px ;
  padding:8px;
  box-sizing: border-box;
}
.nav-item {
  background: no-repeat center center/cover;
  display: flex;
  flex-direction: column;
  justify-content: center;
  border-radius: 6px;
  // box-shadow: 0 5px 20px -8px rgba(0, 0, 0, .5);
  height: 80px;
  color: #ffffff;
  padding: 0 10px 10px;
  .title {
    font-size: 16px;
    font-weight: 700;
    color: #2E3233;
  }
  .sub {
    font-size: 12px;
    opacity:1;
    margin-top: 8px;
    color: #909399;
  }
}
</style>
