<template>
  <div>
    <div class="team-list">
      <div class="caption">{{ $t('title') }}</div>
      <ul class="list">
        <li v-for="item in list" :key="item.id">
          <div class="item">
            <div class="left">
              <div class="id">{{ $t('id') }}：{{ item.uid }}</div>
              <div class="mobile">{{ $t('account') }}：{{ item.mobile }}</div>
              <div v-if="CHEKC_PROXY">{{ $t('level') }}：{{ item.level_name }}</div>
            </div>
            <div class="right">
              <div class="val">{{ $t('profit') }}：{{ Number(item.revenue).toFixed(2) }} USDT</div>
              <!-- <div>{{ $t('yeji') }}：{{ item.total_recharge }} USDT</div> -->
              <div class="time">{{ $t('time') }}：{{ item.ctime }}</div>
              <!-- <a v-if="CHEKC_PROXY_UPDATE && info && info.is_partner==1" @click="changeUserLevel(item.uid)">{{ $t('up_level') }}</a> -->
            </div>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>
<script>
import { mapActions } from 'vuex'
import { CHEKC_PROXY_UPDATE } from '@/config/index'
export default {
  i18n: {
    messages: {
      zh: {
        title: '邀请列表',
        id: '用户ID',
        account: '账号',
        level: '级别',
        profit: '量化盈利',
        time: '时间',
        yeji: '推广业绩',
        up_level: '提升用户级别'
      },
      en: {
        title: 'Invitation list',
        id: 'User ID',
        account: 'Account',
        level: 'Level',
        profit: 'Profit',
        time: 'Time',
        yeji: 'Performance',
        up_level: 'Up Level'
      },
      hk: {
        title: '邀請列表',
        id: '用户ID',
        account: '賬號',
        level: '級別',
        profit: '量化盈利',
        time: '時間',
        yeji: '推廣業績',
        up_level: '提升用戶級別'
      }
    }
  },
  props: {
    info: {
      type: Object,
      required: true,
      default: () => {
        return {}
      }
    }
  },
  data () {
    return {
      CHEKC_PROXY_UPDATE,
      list: ''
    }
  },
  beforeMount () {
    this.loadData()
  },
  methods: {
    ...mapActions({
      invitationList: 'user/invitationList',
      changeLevel: 'user/changeLevel'
    }),
    loadData () {
      this.invitationList()
        .then((data) => {
          this.list = data.data.list
        })
    },
    changeUserLevel(uid) {
      this.$dialog.confirm({
        title: this.$t('msg.Do_you_want_to_upgrade_the_user_level') // '是否要提升该用户等级？'
      })
        .then(() => {
          this.changeLevel({ uid }).then((res) => {
            this.$toast.success(res.msg)
            this.loadData()
          }).catch((res) => {
            this.$toast.fail(res.msg)
          })
        })
    }
  }
}
</script>
<style scoped lang="less">
.team-list {background-color: #fff;}
.team-list .caption {
  font-size: 16px;
  font-weight: 500;
  padding: 10px 15px;
  border-bottom: 1px solid #eee;
}
.team-list .list {
  overflow: hidden;
  padding: 0 15px;
}
.team-list li {
  padding: 10px 0;
  border-top: 1px solid #eee;
}
.team-list .item {
  display: flex;
  justify-content: space-between;
  line-height: 1.8;
  font-size: 12px;
  a {
    color: @themeColor;
  }
}
.team-list li:first-child {
  border-top: none;
}
.team-list .right {
  text-align: right;
}
.team-list .mobile {
  opacity: 0.8;
}
</style>
