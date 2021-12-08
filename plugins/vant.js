import Vue from 'vue'
import {
  Row,
  Col,
  Icon,
  Image,
  Cell,
  CellGroup,
  Button,
  Tab,
  Tabs,
  List,
  Checkbox,
  CheckboxGroup,
  Progress,
  Tag,
  ActionSheet,
  NavBar,
  Dialog,
  Form,
  Field,
  Toast,
  PullRefresh,
  Popup,
  Empty,
  Picker,
  RadioGroup, Radio,
  Locale
} from 'vant'

import enUS from 'vant/es/locale/lang/en-US'

Vue.use(Row)
  .use(Col)
  .use(Image)
  .use(Icon)
  .use(Cell)
  .use(CellGroup)
  .use(Button)
  .use(Tab)
  .use(Tabs)
  .use(Checkbox)
  .use(CheckboxGroup)
  .use(Progress)
  .use(Tag)
  .use(ActionSheet)
  .use(NavBar)
  .use(Dialog)
  .use(Form)
  .use(Field)
  .use(Toast)
  .use(List)
  .use(PullRefresh)
  .use(Popup)
  .use(Empty)
  .use(Picker)
  .use(Radio)
  .use(RadioGroup)
  .use('en-US', enUS)
