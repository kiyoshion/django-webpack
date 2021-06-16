import axios from 'axios'

const csrftoken = document.cookie.split('; ').find(row => row.startsWith('csrftoken')).split('=')[1]

const like = () => {
  const likes = document.querySelectorAll('.js-like')

  likes.forEach((el) => {
    el.addEventListener('click', (e) => {
      let data = new FormData()
      const itemId = el.getAttribute('data-itemid')
      const islike = el.getAttribute('data-islike')
      data.append('pk', itemId)
      data.append('csrfmiddlewaretoken', csrftoken)

      axios.post(`/item/like/${itemId}/`, data)
        .then(res => {
          el.querySelector('span').textContent = res.data.cnt
          if (islike === 'True') {
            el.classList.remove('text-red-300')
            el.classList.add('text-gray-400')
            el.setAttribute('data-islike', 'False')
          } else {
            el.classList.remove('text-gray-400')
            el.classList.add('text-red-300')
            el.setAttribute('data-islike', 'True')
          }
        })
    })
  })
}

const del = (id) => {
  const btnDel = document.querySelector('#btn-del'),
        itemId = id

  btnDel.addEventListener('click', () => {
    let result = window.confirm('アイテムを削除しますか？')
    let data = new FormData()
    data.append('pk', itemId)
    data.append('csrfmiddlewaretoken', csrftoken)

    if (result) {
      axios.post(`/item/del/${itemId}/`, data)
        .then(res => {
          if (res.data.msg === 'ok') {
            location.href = '/item/'
          }
        })
        .catch(err => {
          console.log(err)
        })
    } else {
      return false
    }
  })
}

const sort = (el) => {
  const sort = document.querySelector(el),
        params = new URLSearchParams(window.location.search),
        str = params.get('sort')

  sort.value = str ? str : 'created_at'
  sort.addEventListener('change', () => {
    location.href = `/item/?sort=${sort.value}`
  })
}

export default {
  like,
  del,
  sort,
}
