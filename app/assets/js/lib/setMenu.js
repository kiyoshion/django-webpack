export default () => {
  const menuAvatar = document.querySelector('.menu-avatar')
  const menuUser = document.querySelector('.menu-user')
  if (document.querySelectorAll('.menu-avatar').length) {
    menuAvatar.addEventListener('click', () => {
      menuUser.classList.toggle('is-active')
    })
  }

  const menuBtn = document.querySelector('.menu-btn')
  const menuArea = document.querySelector('.menu-area')
  if (document.querySelectorAll('.menu-btn').length) {
    menuBtn.addEventListener('click', () => {
      menuArea.classList.toggle('is-active')
    })
  }

  const menuBtnClose = document.querySelector('.menu-btn-close')
  if (document.querySelectorAll('.menu-btn-close').length) {
    menuBtnClose.addEventListener('click', () => {
      menuArea.classList.toggle('is-active')
    })
  }
}
