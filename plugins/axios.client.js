import qs from 'qs'
import { tokenStorage } from '~/utils/storage'
export default function ({ store, $axios, redirect }) {
  $axios.setHeader('XX-Device-Type', 'web')
  $axios.setHeader('Content-Type', 'application/x-www-form-urlencoded', ['post'])
  $axios.onRequest((config) => {
    const params = {
      language: ['zh', 'tw'].includes(store.state.locale) ? 'zh_cn' : 'en_us',
      ...config.data
    }
    if (!config.headers['XX-Token']) {
      const accessToken = tokenStorage.get() || ''
      store.commit('user/SET_USER_TOKEN', accessToken)
      $axios.setHeader('XX-Token', accessToken)
    }
    if (config.headers['Content-Type'] !== 'multipart/form-data') { config.data = qs.stringify(params) }
  })
  $axios.onResponse(({ data }) => {
    // return Promise.resolve(data)
    const { code } = data
    if (code === 10001) {
      redirect('/sign/login')
    }
    if (code !== 1) {
      return Promise.reject(data)
    }
  })

  $axios.onError((error) => {
    const { code } = error
    if (code === 10001) {
      redirect('/sign/login')
    }
  })
}
