const addEventListenerToAll = (selector, event, handler) => {
  document.querySelectorAll(selector).forEach(el => {
    el.addEventListener(event, handler)
  })
}

export { addEventListenerToAll }
