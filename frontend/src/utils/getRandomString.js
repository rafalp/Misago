export const ALPHA = "12345678990abcdefghijklmnopqrstuvwxyz"
export const ALPHA_LEN = ALPHA.length

export default function getRandomString(len) {
  const chars = []
  for (let i = 0; i < len; i++) {
    const index = Math.floor(Math.random() * ALPHA_LEN)
    chars.push(ALPHA[index])
  }
  return chars.join("")
}
