export function deleteElement(element, callback) {
  element.classList.remove("animation-fade-in")

  element
    .querySelectorAll("button, input, select, textarea")
    .forEach((child) => {
      child.setAttribute("disabled", "")
    })

  element.addEventListener("animationend", ({ animationName }) => {
    if (animationName === "deleteElementAnimation") {
      element.remove()

      if (callback) {
        callback()
      }
    }
  })

  element.classList.add("animation-delete")
}

export function slideUpElement(element, options) {
  element
    .querySelectorAll("button, input, select, textarea")
    .forEach((child) => {
      child.setAttribute("disabled", "")
    })

  element.classList.add("animation-slide-up")

  const duration = (options && options.duration) || 350
  const height = element.clientHeight
  const opacity = element.style.opacity || 1

  let start
  element.style.overflow = "hidden"

  function onFrame(timestamp) {
    if (start === undefined) {
      start = timestamp
    }

    const progress = Math.min((timestamp - start) / duration, 1)
    const animation = Math.sin(((1 - progress) * Math.PI) / 2)

    element.style.height = Math.floor(height * animation) + "px"
    element.style.opacity = opacity * animation

    if (progress < 1) {
      requestAnimationFrame(onFrame)
    } else {
      element.remove()

      if (options && options.callback) {
        options.callback()
      }
    }
  }

  requestAnimationFrame(onFrame)
}
