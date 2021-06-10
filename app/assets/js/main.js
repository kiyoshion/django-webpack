import '../css/main.scss'

const reqImg = (r = require.context('../img', true)) => r.keys().forEach(r)
reqImg()
