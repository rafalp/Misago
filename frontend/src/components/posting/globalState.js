export function getGlobalState() {
  return window.misagoReply
}

export function setGlobalState(disabled, quote) {
  window.misagoReply = { disabled, quote }
}

export function clearGlobalState() {
  window.misagoReply = null
}
