document.body.addEventListener("click", (event) => {
  const target = event.target.closest("[misago-scroll-to]")
  if (!!target) {
    const selector = target.getAttribute("misago-scroll-to")
    const element = document.querySelector(selector)
    if (element) {
      event.preventDefault()
      element.scrollIntoView({ behavior: "instant" })
    }
  }
})
