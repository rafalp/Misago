export default function (string, subString) {
  string = (string + "").toLowerCase()
  subString = (subString + "").toLowerCase()

  if (subString.length <= 0) return 0

  let n = 0
  let pos = 0
  let step = subString.length

  while (true) {
    pos = string.indexOf(subString, pos)
    if (pos >= 0) {
      n += 1
      pos += step
    } else {
      break
    }
  }

  return n
}
