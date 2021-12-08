import Vue from 'vue'
import VueI18n from 'vue-i18n'
import enLocale from '@/locales/en'
import zhLocale from '@/locales/zh'
import { langStorage } from '@/utils/storage'

Vue.use(VueI18n)

const messages = {
  en: enLocale,
  zh: zhLocale
}
const locales = Object.keys(messages)

export default ({ app, store, route }) => {
  // 跟随系统：navigator.language.split('-')[0]
  let locale = route.query.lang
  const fallbackLocale = 'zh'
  if (locale && locales.includes(locale)) {
    store.dispatch('setLang', locale)
  } else {
    locale = langStorage.get()
    if (!locale) {
      locale = navigator.language.split('-')[0]
      store.dispatch('setLang', locale)
    }
  }

  // Set i18n instance on app
  // This way we can use it in middleware and pages asyncData/fetch
  app.i18n = new VueI18n({
    locale: store.state.locale,
    fallbackLocale,
    messages
  })
}
