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

export function useLoader(target) {
  const silent = target.closest("[hx-silent]")
  if (silent) {
    return silent.getAttribute("hx-silent") !== "true"
  }

  return true
}

export default AjaxLoader
