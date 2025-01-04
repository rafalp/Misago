document.body.addEventListener("click", (event) => {
  const selector = event.target.getAttribute("misago-focus-on")
  if (!!selector) {
    event.preventDefault()
    const element = document.querySelector(selector)
    if (element) {
      element.focus()
    }
  }
})
