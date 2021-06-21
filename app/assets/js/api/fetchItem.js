import axios from 'axios'

const csrftoken = document.cookie.split('; ').find(row => row.startsWith('csrftoken')).split('=')[1]

const like = () => {
  const likes = document.querySelectorAll('.js-like')

  likes.forEach((el) => {
    el.addEventListener('click', (e) => {
      const itemId = el.getAttribute('data-itemid')
      const islike = el.getAttribute('data-islike')
      if (islike === '1' || islike === '0') {
        let data = new FormData()
        data.append('pk', itemId)
        data.append('csrfmiddlewaretoken', csrftoken)

        axios.post(`/item/like/${itemId}/`, data)
          .then(res => {
            el.querySelector('span').textContent = res.data.cntAll
            if (res.data.cntCurrent === 0) {
              el.classList.remove('is-like')
              el.setAttribute('data-islike', 0)
            } else {
              el.classList.add('is-like')
              el.setAttribute('data-islike', 1)
            }
          })
      }
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

const sort = (el, ...tag) => {
  const sort = document.querySelector(el),
        params = new URLSearchParams(window.location.search),
        str = params.get('sort')

  sort.value = str ? str : 'created_at'
  sort.addEventListener('change', () => {
    if (tag.length > 0) {
      const tagId = tag[0]
      location.href = `/item/tag/${tagId}/?sort=${sort.value}`
    } else {
      location.href = `/item/?sort=${sort.value}`
    }
  })
}

export default {
  like,
  del,
  sort,
}
