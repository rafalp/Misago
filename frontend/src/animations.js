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
