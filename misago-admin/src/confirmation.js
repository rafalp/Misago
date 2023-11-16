const initConfirmation = (selector, message) => {
  const elements = document.querySelectorAll(selector)
  const handler = event => {
    if (!window.confirm(message)) {
      event.preventDefault()
      return false
    }
  }

  elements.forEach(el => {
    const eventName = el.tagName.toLowerCase() === "form" ? "submit" : "click"
    el.addEventListener(eventName, handler)
  })
}

export default initConfirmation
