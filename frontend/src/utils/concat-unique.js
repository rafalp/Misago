export default function (a, b) {
  let ids = []
  return a.concat(b).filter(function (item) {
    if (ids.indexOf(item.id) === -1) {
      ids.push(item.id)
      return true
    } else {
      return false
    }
  })
}
