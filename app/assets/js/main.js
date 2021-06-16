import '../css/main.css'
import "@yaireo/tagify/dist/tagify.css"
// import './loadVueComponent'
import './loadFontAwesome'

const path = location.pathname
const header = document.querySelector('.header')
const footer = document.querySelector('.footer')
if (path.match(/account/)) {
  const jsBlur = document.querySelector('.js-blur')
  if (jsBlur) {
    jsBlur.classList.add('bg-blur')
    jsBlur.style.backgroundImage = `url("/static/img/bg-0.jpg")`
    jsBlur.style.minHeight = `calc(100vh - ${header.clientHeight + footer.clientHeight}px)`
  }
}
