import { dom, library } from '@fortawesome/fontawesome-svg-core'
import { faEnvelope, faLock, faHeart, faCamera, faCalendarAlt, faPencilAlt, faTrashAlt, faInfoCircle, faComment, faUser, faAngleLeft, faAngleRight } from '@fortawesome/free-solid-svg-icons'

const set = library.add(faEnvelope, faLock, faHeart, faCamera, faCalendarAlt, faPencilAlt, faTrashAlt, faInfoCircle, faComment, faUser, faAngleLeft, faAngleRight)
const watch = dom.watch()

export default {
  set,
  watch
}
