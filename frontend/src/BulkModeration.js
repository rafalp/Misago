import htmx from "htmx.org"

class BulkModeration {
  constructor(options) {
    this.formId = options.formId
    this.modal = options.modal
    this.actions = options.actions
    this.selection = options.selection
    this.button = options.button

    this.update()
    this.registerEvents()
    this.registerActions()
  }

  registerActions = () => {
    this.actions.forEach(element => {
      element.addEventListener("click", this.onAction)
    });
  }

  onAction = (event) => {
    const form = document.getElementById(this.formId)
    const data = {};

    (new FormData(form)).forEach((value, key) => {
      if (typeof data[key] === "undefined") {
        data[key] = []
      }
      data[key].push(value)
    })

    const target = event.target
    data.moderation = target.getAttribute("moderation-action")
    
    if (target.getAttribute("moderation-two-step") === "true") {
      htmx.ajax(
        "POST",
        document.location.href,
        {
          target: this.modal,
          swap: "innerHTML",
          values: data,
        }
      ).then(() => {
        $(this.modal).modal("show")
      })
    } else {
      htmx.ajax(
        "POST",
        document.location.href,
        {
          target: "#misago-htmx-root",
          swap: "outerHTML",
          values: data,
        }
      )
    }
  }

  registerEvents = () => {
    document.body.addEventListener("click", ({ target }) => {
      if(target.tagName === "INPUT" && target.type === "checkbox") {
        this.update()
      }
    })

    htmx.onLoad(() => this.update())
  }

  update = () => {
    const selection = document.querySelectorAll(this.selection).length

    if (selection) {
      this.button.element.innerText = this.button.selected.replace("%(number)s", selection)
    } else {
      this.button.element.innerText = this.button.default
    }

    this.button.element.disabled = !selection
  }
}

export default BulkModeration