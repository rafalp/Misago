const ALPHABET =
  "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
const ALPHABET_LENGTH = ALPHABET.length

export default function getRandomString(length) {
  let string = ""
  for (let i = 0; i < length; i++) {
    string += ALPHABET[Math.floor(Math.random() * ALPHABET_LENGTH)]
  }
  return string
}
