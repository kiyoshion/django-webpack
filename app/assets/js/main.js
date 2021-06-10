import '../css/main.scss'

const reqImg = (r = require.context('../img', true)) => r.keys().forEach(r)
reqImg()

console.log('Hello webpack!!!')
console.log('Hello Django!!!')
