import Tagify from '@yaireo/tagify'

export default (el, ...[tagArr]) => {
  const tags = document.querySelector(el),
        tagify = new Tagify(tags, {
          originalInputValueFormat: valuesArr => valuesArr.map(item => item.value).join(',')
        })

  const currentTags = tagArr && tagArr.replace(/\[|&#x27;|\]/g, '')

  if (tagArr) {
    tagify.removeAllTags()
    tagify.addTags(currentTags)
  }

}
