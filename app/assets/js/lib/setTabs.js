export default () => {
  const tabList = document.querySelectorAll('.tab-list > div'),
        tabItems = document.querySelectorAll('.tab-items > div')

  tabList.forEach(clickedItem => {
    clickedItem.addEventListener('click', e => {
      e.preventDefault()

      tabList.forEach(list => {
        list.classList.remove('js-current')
      })

      clickedItem.classList.add('js-current')

      tabItems.forEach(item => {
        item.classList.remove('block')
        item.classList.add('hidden')
      })

      document.getElementById(clickedItem.dataset.id).classList.remove('hidden')
      document.getElementById(clickedItem.dataset.id).classList.add('block')
    })
  })

}
