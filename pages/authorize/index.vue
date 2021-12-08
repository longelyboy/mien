<template>
  <div>
    <van-nav-bar
      :title="$t('homeMenu.item1.title')"
      left-arrow
      @click-left="$router.back()"
    />
    <div class="list">
      <van-cell
        v-for="(item, index) in platform"
        :key="item.name"
        @click="item.disabledEdit ? () => {} : openSheet(index)"
      >
        <van-row
          type="flex"
          align="center"
          justify="space-between"
          class="item"
        >
          <van-col>
            <van-image
              class="logo"
              :class="{[item.label]: true}"
              :src="item.logo"
            />
          </van-col>
          <van-col style="flex: 1">
            <div class="name">{{ $t(item.label) }}</div>
          </van-col>
          <van-col>
            <van-icon
              v-if="!item.disabledEdit"
              style="vertical-align: middle"
              name="ellipsis"
              size="20"
            />
          </van-col>
        </van-row>
      </van-cell>
    </div>
    <van-action-sheet
      v-model="show"
      :cancel-text="$t('actions.cancel')"
      close-on-click-action
    >
      <div class="sheet-title">
        <van-image class="logo" :src="platform[active].logo" />
        <span>{{ $t(platform[active].label) }}</span>
        <span v-if="!platform[active].api_key" class="tip" >{{ $t('not') }}</span>
        <span v-if="platform[active].status === -1" class="tip error" >{{ $t('expired') }}</span>
      </div>
      <van-cell-group>
        <template v-if="platform[active].api_key">
          <van-cell @click="viewApi">{{ $t('actions.view') }}</van-cell>
          <van-cell :to="'/authorize/form?active='+active">{{ $t('actions.edit') }}</van-cell>
          <van-cell @click="removeApi">{{ $t('actions.del') }}</van-cell>
        </template>
        <template v-else>
          <van-cell :to="'/authorize/form?active='+active">{{ $t('add') }}</van-cell>
        </template>
      </van-cell-group>
    </van-action-sheet>

    <van-popup
      v-model="showApi"
      class="api-popup"
      @close="closeApiPop"
    >
      <div class="sheet-title">
        <van-image
          class="logo"
          :src="platform[active].logo"
        />
        <span>{{ platform[active].name }}</span>
        <span
          v-if="platform[active].status === -1"
          class="tip error"
        >{{ $t('expired') }}</span>
      </div>
      <div class="api">{{ api }}</div>
    </van-popup>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
export default {
  i18n: {
    messages: {
      zh: {
        add: '添加API Key',
        not: '您还未添加该平台的API',
        expired: '该平台的API已失效'
      },
      en: {
        add: 'Add API Key',
        not: 'You have not added the platform\'s API',
        expired: 'The platform\'s API is no longer available'
      }
    }
  },
  data () {
    return {
      show: false,
      showApi: false,
      api: '',
      active: 0,
      actions: [{ name: '查看API Key' }, { name: '删除' }, { name: '重置' }]
    }
  },
  computed: {
    ...mapState({
      platform: ({ authorize }) => authorize.platform
    })
  },
  mounted () {
    this.getData()
  },
  methods: {
    ...mapActions({
      getApiAccount: 'authorize/getApiAccount',
      removeApiAccount: 'authorize/removeApiAccount',
      setApiInfo: 'authorize/setApiInfo'
    }),
    getData() {
      this.platform.forEach((item, index) => {
        this.getApiAccount({ platform: item.label }).then((res) => {
          this.setApiInfo([index, res.data])
        }).catch(() => { })
      })
    },
    openSheet (index) {
      this.active = index
      this.show = true
    },
    viewApi () {
      this.show = false
      this.api = this.platform[this.active].api_key
      this.showApi = true
    },
    closeApiPop () {
      this.showApi = false
      this.$nextTick(() => {
        this.api = ''
      })
    },
    removeApi () {
      this.show = false
      this.$dialog.confirm({
        message: '确定删除此平台API？'
      }).then((res) => {
        this.$toast.loading()
        this.removeApiAccount({ platform: this.platform[this.active].label }).then((res) => {
          this.$toast(res.msg)
          this.getData()
        }).catch(({ msg }) => this.$toast(msg))
      })
    }
  }
}
</script>

<style scoped lang="less">
.item {
  background-color: #fff;
}
.logo {
  width: 50px;
  display: block;
  &.sinance {
    img {
      width: 40px;
      height: 40px;
      margin: auto;
      display: block;
    }
  }
}
.name {
  font-weight: 500;
}
.tip {
  font-size: 12px;
  opacity: 0.8;
  margin-top: 5px;
}
.error {
  color: red;
}
.sheet-title {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-size: 18px;
  padding: 20px 0;
  .logo {
    display: inline-block;
  }
}
.api-popup {
  width: 80vw;
  text-align: center;
  .api {
    font-weight: 600;
    margin-bottom: 30px;
  }
}
</style>
