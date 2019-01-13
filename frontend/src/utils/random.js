export function int(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min
}

export function range(min, max) {
  let array = new Array(int(min, max))
  for (let i = 0; i < array.length; i++) {
    array[i] = i
  }

  return array
}
