export default (img, preview) => {
  const elImg = document.querySelector(img),
        elPreview = document.querySelector(preview)

  elImg.addEventListener('change', (event) => {
    const file = event.target.files[0]
    const render = new FileReader()
    render.onload = () => {
      const newImg = new Image()
      newImg.src = render.result
      elPreview.setAttribute('src', newImg.src)
    }
    render.readAsDataURL(file)
  })
}
