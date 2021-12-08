<template>
  <van-notice-bar style="background:#fff;color:#333;" left-icon="volume-o" :scrollable="false">
    <van-swipe vertical class="notice-swipe" :autoplay="3000" :show-indicators="false">
      <van-swipe-item v-for="item in notice" :key="item.id">
        <div class="van-ellipsis" @click="viewDetail(item)">
          {{ item.post_title }}
        </div>
      </van-swipe-item>
    </van-swipe>
  </van-notice-bar>
</template>

<script>
import { Swipe, SwipeItem, NoticeBar } from 'vant'
import { mapActions } from 'vuex'
export default {
  components: {
    [Swipe.name]: Swipe,
    [SwipeItem.name]: SwipeItem,
    [NoticeBar.name]: NoticeBar
  },
  data () {
    return {
      notice: []
    }
  },
  mounted () {
    this.getNotice({ type: 1 }).then((res) => {
      this.notice = res.data.list
    })
  },
  methods: {
    ...mapActions({
      getNotice: 'getNotice'
    }),
    viewDetail (item) {
      this.$router.push({
        name: 'common-article',
        params: {
          url: item.visit_url,
          title: item.post_title
        }
      })
    }
  }
}
</script>

<style scoped lang="less">
.notice-swipe {
  height: 40px;
  line-height: 40px;
}
/deep/ .van-notice-bar__content {
  width: 100%;
}

/deep/ .van-notice-bar__left-icon, /deep/ .van-notice-bar__right-icon{
 color:#1778fc;
}
</style>
