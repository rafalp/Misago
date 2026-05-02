import htmx from "htmx.org"
import { mountTemplate } from "./template"

class BulkModeration {
  constructor(options) {
    this.actions = document.querySelectorAll(options.actions)
    this.control = document.querySelector(options.button.selector)
    this.form = options.form
    this.menu = options.menu ? document.querySelector(options.menu) : null
    this.modal = options.modal
    this.selection = options.selection
    this.target = options.target || "#misago-htmx-root"
    this.text = options.button.text

    this.update()
    this.registerEvents()
    this.registerActions()
  }

  registerActions = () => {
    this.actions.forEach((element) => {
      if (element.getAttribute("mg-moderation-action") === "remove-selection") {
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
    data.moderation = target.getAttribute("mg-moderation-action")

    if (target.getAttribute("mg-moderation-multistage") === "true") {
      const modal = document.querySelector(this.modal)
      if (!modal) {
        console.warn(
          "Could not resolve the '" +
            this.modal.selector +
            "' element specified in the 'modal.selector' option."
        )
        return
      }

      const modalTitle = modal.querySelector("[mg-modal-title]")
      if (!modalTitle) {
        console.warn(
          "Could not resolve the '[mg-modal-title]' child element in '" +
            this.modal.selector +
            "'."
        )
        return
      }

      modalTitle.textContent = target.getAttribute("mg-moderation-full-name")

      $(modal).modal("show")

      htmx.ajax("POST", document.location.href, {
        target: this.control.getAttribute("hx-target"),
        swap: "innerHTML",
        source: this.control,
        values: data,
      })
    } else {
      htmx.ajax("POST", document.location.href, {
        target: this.target,
        swap: "outerHTML",
        values: data,
      })
    }
  }

  onRemoveSelection = () => {
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
