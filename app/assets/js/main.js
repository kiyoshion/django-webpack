import '../css/main.css'
import "@yaireo/tagify/dist/tagify.css"
import './loadFontAwesome'
import * as lib from './lib'
import * as api from './api'

window.libs = lib.default
window.fetchItem = api.fetchItem
window.fetchUser = api.fetchUser

lib.default.setBlur('.js-blur', /account/, '/static/img/bg-0.jpg')
lib.default.setMenu()
