<template>
  <div>
    <van-nav-bar
      :title="$t('title')"
      left-arrow
      @click-left="$router.back()"
      @click-right="showPwd = true"
    />
    <van-form @submit="onSubmit">
      <van-field
        v-model="form.country"
        :label="$t('nationality')"
        :placeholder="$t('nationality_please')"
        :rules="[{ required: true, message: $t('nationality_please') }]"
      />
      <van-field
        v-model="form.address"
        :label="$t('address')"
        :placeholder="$t('address_please')"
        :rules="[{ required: true, message: $t('address_please') }]"
      />
      <van-field
        v-model="form.u_name"
        :label="$t('name')"
        :placeholder="$t('name_please')"
        :rules="[{ required: true, message: $t('name_please') }]"
      />
      <van-field
        :value="form.birthday"
        :label="$t('birthday')"
        :placeholder="$t('birthday_please')"
        readonly
        clickable
        :rules="[{ required: true, message: $t('birthday_please') }]"
        @click="showPicker = true"
      />
      <van-field
        v-model="form.photo_id"
        :label="$t('card')"
        :placeholder="$t('card_please')"
        :rules="[{ required: true, message: $t('card_please') }]"
      />
      <van-field :label="$t('card_front')">
        <template #input>
          <van-uploader name="photo_id1" :after-read="afterRead">
            <van-image height="38vw" :src="card_frontend"></van-image>
            <van-image
              v-if="form.photo_id1"
              fit="cover"
              class="preview-cover"
              :src="IMG_BASE_URL + form.photo_id1"
            ></van-image>
          </van-uploader>
        </template>
      </van-field>
      <van-field :label="$t('card_back')">
        <template #input>
          <van-uploader name="photo_id2" :after-read="afterRead">
            <van-image height="38vw" :src="card_backend"></van-image>
            <van-image
              v-if="form.photo_id2"
              fit="cover"
              class="preview-cover"
              :src="IMG_BASE_URL + form.photo_id2"
            ></van-image>
          </van-uploader>
        </template>
      </van-field>
      <div style="padding: 16px">
        <van-button round block type="info" native-type="submit">{{ $t('actions.submit') }}</van-button>
      </div>
    </van-form>
    <van-popup v-model="showPicker" position="bottom">
      <van-datetime-picker
        type="date"
        :min-date="minDate"
        :max-date="maxDate"
        @confirm="onConfirm"
        @cancel="showPicker = false"
      />
    </van-popup>
  </div>
</template>

<script>
import { Uploader, DatetimePicker } from 'vant'
import { mapActions } from 'vuex'
import { format as timeFormat } from '@/utils/time'
import { IMG_BASE_URL } from '@/config/index'
export default {
  components: {
    [Uploader.name]: Uploader,
    [DatetimePicker.name]: DatetimePicker
  },
  i18n: {
    messages: {
      zh: {
        title: '实名认证',
        nationality: '国籍',
        nationality_please: '请填写国籍',
        address: '住址',
        address_please: '请填写住址',
        name: '真实姓名',
        name_please: '请填写真实姓名',
        birthday: '生日',
        birthday_please: '请选择生日',
        card: '身份证号',
        card_please: '请填写身份证号',
        card_front: '身份证正面照',
        card_back: '身份证反面照'
      },
      en: {
        title: 'Real Name',
        nationality: 'Nationality',
        nationality_please: 'Please fill in your nationality',
        address: 'Address',
        address_please: 'Please fill in your address',
        name: 'Real Name',
        name_please: 'Please fill in your real name',
        birthday: 'Birthday',
        birthday_please: 'Please select a birthday',
        card: 'ID number',
        card_please: 'Please fill in the ID number',
        card_front: 'Front of ID card',
        card_back: 'Reverse of ID card'
      },
      hk: {
        title: '實名認證',
        nationality: '國籍',
        nationality_please: '請填寫國籍',
        address: '住址',
        address_please: '請填寫住址',
        name: '真實姓名',
        name_please: '請填寫真實姓名',
        birthday: '生日',
        birthday_please: '請選擇生日',
        card: '身份證號',
        card_please: '請填寫身份證號',
        card_front: '身份證正面照',
        card_back: '身份證反面照'
      }
    }
  },
  data () {
    return {
      IMG_BASE_URL,
      card_frontend: require('@/assets/images/card-frontend.svg'),
      card_backend: require('@/assets/images/card-backend.svg'),
      showPicker: false,
      minDate: new Date(1970, 0, 1),
      maxDate: new Date(),
      form: {
        country: '',
        u_name: '',
        birthday: '',
        photo_id1: '',
        photo_id2: '',
        photo_id: '',
        address: ''
      }
    }
  },
  methods: {
    ...mapActions({
      addAuth: 'user/addAuth',
      upload: 'upload'
    }),
    onSubmit () {
      if (!this.form.photo_id1 || !this.form.photo_id2) {
        this.$toast.fail('请上传身份证照片')
        return
      }
      this.$toast.loading()
      this.addAuth({ ...this.form }).then((res) => {
        this.$toast(res.msg)
        this.$router.back()
      }).catch((res) => { this.$toast(res.msg) })
    },
    onConfirm (value) {
      this.form.birthday = timeFormat(value, '{y}-{m}-{d}')
      this.showPicker = false
    },
    afterRead (file, detail) {
      const toast = this.$toast.loading()
      this.upload(file.file)
        .then((res) => {
          this.form[detail.name] = res.data.url
        })
        .finally(() => {
          toast.clear()
        })
    }
  }
}
</script>

<style scoped lang="less">
.preview-cover {
  position: absolute;
  bottom: 0;
  left: 0;
  box-sizing: border-box;
  width: 100%;
  height: 100%;
}
</style>
