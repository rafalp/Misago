import htmx from "htmx.org"

class BulkModeration {
  constructor(options) {
    this.menu = options.menu ? document.querySelector(options.menu) : null
    this.form = options.form
    this.modal = options.modal
    this.actions = document.querySelectorAll(options.actions)
    this.selection = options.selection
    this.control = document.querySelector(options.button.selector)
    this.text = options.button.text

    this.update()
    this.registerEvents()
    this.registerActions()
  }

  registerActions = () => {
    this.actions.forEach((element) => {
      if (element.getAttribute("moderation-action") === "remove-selection") {
        element.addEventListener("click", this.onRemoveSelection)
      } else {
        element.addEventListener("click", this.onAction)
      }
    })
  }

  onAction = (event) => {
    const form = document.querySelector(this.form)
    const data = {}

    new FormData(form).forEach((value, key) => {
      if (typeof data[key] === "undefined") {
        data[key] = []
      }
      data[key].push(value)
    })

    const target = event.target
    data.moderation = target.getAttribute("moderation-action")

    if (target.getAttribute("moderation-multistage") === "true") {
      htmx
        .ajax("POST", document.location.href, {
          target: this.modal,
          swap: "innerHTML",
          values: data,
        })
        .then(() => {
          $(this.modal).modal("show")
        })
    } else {
      htmx.ajax("POST", document.location.href, {
        target: "#misago-htmx-root",
        swap: "outerHTML",
        values: data,
      })
    }
  }

  onRemoveSelection = (event) => {
    document.querySelectorAll(this.selection).forEach((element) => {
      element.checked = false
    })
    this.update()
  }

  registerEvents = () => {
    document.body.addEventListener("click", ({ target }) => {
      if (target.tagName === "INPUT" && target.type === "checkbox") {
        this.update()
      }
    })

    htmx.onLoad(() => this.update())
  }

  update = () => {
    const selection = document.querySelectorAll(this.selection).length

    this.control.innerText = this.text.replace("%(number)s", selection)
    this.control.disabled = !selection

    if (this.menu) {
      if (selection) {
        this.menu.classList.add("visible")
      } else {
        this.menu.classList.remove("visible")
      }
    }
  }
}

export default BulkModeration
