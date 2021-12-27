<template>
  <div>
    <van-nav-bar :title="$t('pageUser.community')" left-arrow @click-left="$router.back()" >
      <template #right>
        <van-icon name="share-o" size="18" @click="$router.push('/user/invite/poster')" />
      </template>
    </van-nav-bar>

    <div class="referral-info">
      <div class="total">
        <div class="lab">{{ $t('total') }} USDT</div>
        <div class="val">{{ Number(info.total_all_sum).toFixed(5) || 0 }} </div>
      </div>
      <div class="reg">{{ $t('invite') }} {{ info.total_reg_count }} 人</div>
      <div class="items">
        <div class="item">
          <div class="val">{{ info.count_reg_1 }}</div>
          <div class="lab">{{ $t('number_1') }}</div>
        </div>
        <div class="item">
          <div class="val">{{ info.count_reg_2 }}</div>
          <div class="lab">{{ $t('number_2') }}</div>
        </div>
      </div>
    </div>
    <div v-if="info && CHEKC_PROXY" class="user-info">
      <div v-if="CHEKC_HEHUO" class="tag">
        {{ $t('agent') }}：{{ info.my_info.is_partner === 1 ? $t('yes') : $t('no') }}
      </div>
      <van-row class="info" type="flex" justify="space-between">
        <van-col :span="8"><p class="label">{{ $t('you_level') }}</p><p class="value">{{ info.my_info.level_name }}</p></van-col>
        <van-col :span="8"><p class="label">{{ $t('ratio') }}</p><p class="value">{{ info.my_info.profit_rate }}%</p></van-col>
        <van-col :span="8"><p class="label">{{ $t('result') }}</p><p class="value">{{ info.my_info.total }} USDT</p></van-col>
      </van-row>
    </div>
    <referralRank :info="info.my_info" />
  </div>
</template>

<script>
import { mapActions } from 'vuex'
import referralRank from './components/ReferralRank'
import { CHEKC_PROXY, CHEKC_HEHUO } from '@/config/index'
export default {
  i18n: {
    messages: {
      zh: {
        total: '累计邀请分润奖励',
        invite: '好友邀请人数',
        active: '好友激活人数',
        number: '好友注册人数',
        number_1: '一级好友数',
        number_2: '二级好友数',
        number_3: '其余好友数',
        you_level: '代理身份',
        partner: '合伙人',
        user: '用户',
        agent: '合伙人身份',
        ratio: '分润比例',
        result: '总推广业绩',
        yes: '是',
        no: '否'
      },
      en: {
        total: 'Cumulative Invitation Registration Bonus',
        invite: 'Number of friends inviting',
        active: 'Number of friends activating',
        number: 'Number of friends registered',
        number_1: 'Number of first-level friends',
        number_2: 'Number of secondary friends',
        number_3: 'Number of third-level friends',
        you_level: 'Agent identity',
        partner: 'Partner',
        user: 'User',
        agent: 'Partner status',
        ratio: 'Dividend ratio',
        result: 'Performance',
        yes: '是',
        no: '否'
      },
      hk: {
        total: '累計邀請分潤獎勵',
        invite: '好友邀請人數',
        active: '好友激活人數',
        number: '好友註冊人數',
        number_1: '一級好友數',
        number_2: '二級好友數',
        number_3: '其餘好友數',
        you_level: '代理身份',
        partner: '合伙人',
        user: '用户',
        agent: '合伙人身份',
        ratio: '分潤比例',
        result: '總推廣業績',
        yes: '是',
        no: '否'
      }
    }
  },
  components: { referralRank },
  data () {
    return {
      CHEKC_PROXY,
      CHEKC_HEHUO,
      info: ''
    }
  },
  mounted () {
    this.invitationInfo()
      .then((data) => {
        this.info = data.data
      })
  },
  methods: {
    ...mapActions({
      invitationInfo: 'user/invitationInfo'
    })
  }
}
</script>

<style scoped lang="less">
.referral-info {
  margin: 15px;
  padding: 0 10px;
  border-radius: 10px;
  background: rgb(66, 65, 65);
  text-align: center;
  line-height: 25px;
}
.referral-info .total {
  padding: 20px 20px 10px;
}
.referral-info .total .lab {
  color: #fff;
  font-size: 14px;
}
.referral-info .total .val {
  color:#FFDF2F;
  font-size: 24px;
}
.referral-info .total .val {
  font-weight: bold;
}
.referral-info .items {
  border-top: 1px solid rgba(255, 255, 255, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px 0;
}
.referral-info .item {
  flex: 1 0 0;
}
.referral-info .item .val {
  font-size: 15px;
  font-weight: bold;
  color: #fff;
}
.referral-info .item .lab {
  font-size: 14px;
  color: #fff;
  margin-top: 5px;
}
.reg {
  color: #fff;
  padding-bottom: 15px;
  font-size: 14px;
}
.user-info {
  // background: linear-gradient(45deg, #ffe57f, rgb(255, 219, 41));
  background-color: #fff;
  margin-bottom: 15px;
  padding: 10px 15px;
  .tag {
    font-size: 16px;
    margin: 0 -15px 10px;
    padding: 0 15px 10px;
    border-bottom: 1px solid #eee;
  }
  .van-col ~ .van-col {
    position: relative;
    &::before {
      content: '';
      position: absolute;
      top: 15%;bottom: 15%;left: 0;
      width: 1px;background-color: #bbb;
      transform: scaleX(.5);
    }
  }
  .info {
    padding: 10px 0;
    text-align: center;
  }
  .label {
    margin-bottom: 10px;
    font-size: 12px;
  }
  .value {
    font-size: 16px;
    color: #666;
  }
}
</style>
