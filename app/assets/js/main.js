import '../css/main.css'
import "@yaireo/tagify/dist/tagify.css"
import './loadFontAwesome'
import * as lib from './lib'
import * as api from './api'

window.libs = lib.default
window.fetchItem = api.fetchItem
window.fetchUser = api.fetchUser

const path = location.pathname
const header = document.querySelector('.header')
const footer = document.querySelector('.footer')
if (path.match(/account/)) {
  const jsBlur = document.querySelector('.js-blur')
  const imgPath = '/static/img/bg-0.jpg'
  if (jsBlur) {
    jsBlur.classList.add('bg-blur')
    jsBlur.style.backgroundImage = `url("${imgPath}")`
    jsBlur.style.minHeight = `calc(100vh - ${header.clientHeight + footer.clientHeight}px)`
  }
}
