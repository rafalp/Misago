document.body.addEventListener("click", (event) => {
  const selector = event.target.getAttribute("misago-scroll-to")
  if (!!selector) {
    event.preventDefault()
    const element = document.querySelector(selector)
    if (element) {
      element.scrollIntoView({ behavior: "instant" })
    }
  }
})
