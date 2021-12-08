import Vue from 'vue'
import * as time from '@/utils/time'
import * as number from '@/utils/number'

function createFilterRegister (Vue) {
  return (name, fn) => {
    Vue.filter(name, fn)
  }
}

export default function ({ store: { state } }) {
  const allFilters = {
    numberFormat: number.format,
    priceFormat: number.priceFormat,
    currency: number.currency,
    timeFormat: time.format
  }
  const filterRegister = createFilterRegister(Vue)
  Object.keys(allFilters).forEach((name) => {
    filterRegister(name, allFilters[name])
  })
}
