import {
  getClosestAttribute,
  getClosestBoolAttribute,
} from "./closest-attribute"

class AjaxLoader {
  constructor() {
    this.element = document.getElementById("misago-ajax-loader")
    this.requests = 0
    this.timeout = null
  }

  show = () => {
    this.requests += 1
    this.update()
  }

  hide = () => {
    if (this.requests) {
      this.requests -= 1
      this.update()
    }
  }

  update = () => {
    if (this.timeout) {
      window.clearTimeout(this.timeout)
    }

    if (this.requests) {
      this.element.classList.add("busy")
      this.element.classList.remove("complete")
    } else {
      this.element.classList.remove("busy")
      this.element.classList.add("complete")

      this.timeout = setTimeout(() => {
        this.element.classList.remove("complete")
      }, 1500)
    }
  }
}

function useLoader(target) {
  const loader = getClosestAttribute(target, "mg-loader")
  if (!loader || loader === "true") {
    return true
  }
  return false
}

const loader = new AjaxLoader()

document.addEventListener("htmx:beforeRequest", ({ target }) => {
  if (useLoader(target)) {
    loader.show()
  }
})

document.addEventListener("htmx:afterRequest", ({ target }) => {
  if (useLoader(target)) {
    loader.hide()
  }
})

export default loader
