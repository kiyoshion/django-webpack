import axios from 'axios'

const csrftoken = document.cookie.split('; ').find(row => row.startsWith('csrftoken')).split('=')[1]

const setAvatar = (uid) => {

  const elAvatar = document.querySelector('#avatar'),
        elImg = document.querySelector('#avatar > img'),
        elInput = document.querySelector('#input'),
        userId = uid

  elAvatar.addEventListener('click', () => {
    elInput.click()
    return false
  })

  elInput.addEventListener('change', () => {
    let data = new FormData()
    let file = elInput.files[0]
    data.append('avatar', file)
    data.append('csrfmiddlewaretoken', csrftoken)

    axios.post(`/user/avatarupload/${userId}/`, data, {
      headers: {
        'content-type': 'multipart/form-data'
      }
    })
      .then(res => {
        setNewAvatar(res.data.url)
      })
      .catch(error => console.log(error))
  })

  function setNewAvatar(url) {
    elImg.src = url
  }
}

export default {
  setAvatar,
}
