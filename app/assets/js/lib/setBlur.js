export default (target, str, img) => {
  const path = location.pathname
  const header = document.querySelector('.header')
  const footer = document.querySelector('.footer')

  if (path.match(str)) {
    const jsBlur = document.querySelector(target)
    const imgPath = img
    if (jsBlur) {
      jsBlur.classList.add('bg-blur')
      jsBlur.style.backgroundImage = `url("${imgPath}")`
      jsBlur.style.minHeight = `calc(100vh - ${header.clientHeight + footer.clientHeight}px)`
    }
  }
}
