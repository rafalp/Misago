export function push(array, value) {
  if (array.indexOf(value) === -1) {
    let copy = array.slice()
    copy.push(value)
    return copy
  } else {
    return array
  }
}

export function remove(array, value) {
  if (array.indexOf(value) >= 0) {
    return array.filter(function (i) {
      return i !== value
    })
  } else {
    return array
  }
}

export function toggle(array, value) {
  if (array.indexOf(value) === -1) {
    let copy = array.slice()
    copy.push(value)
    return copy
  } else {
    return array.filter(function (i) {
      return i !== value
    })
  }
}
