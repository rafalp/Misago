import htmx from "htmx.org"
import { clearFieldError } from "./fieldError"

class UserSelect {
  constructor(options) {
    const { input } = options

    this.options = options
    this.input = input

    this.container = this.createContainer(input)
    this.dropdown = this.createDropdown()
    
    const name = input.getAttribute("name")
    input.setAttribute("name", name + "_off")
    input.setAttribute("autocomplete", "off")

    this.hidden = this.createHiddenInput(name)
    this.choice = null
    this.clear = null

    this.topChoiceSelected = false

    this.setupHtmx()

    input.addEventListener("focus", () => {
      this.showDropdown()
    })

    input.addEventListener("keydown", (event) => {
      if (event.code === "Escape") {
        if (this.dropdownIsOpen()) {
          this.hideDropdown()
          event.preventDefault()
          event.stopPropagation()
        }
      } else {
        this.showDropdown()
      }
  
      if (event.code === "ArrowDown") {
        const firstChoice = this.dropdown.querySelector("button")
        if (firstChoice) {
          firstChoice.focus()
          this.topChoiceSelected = true
        }
      }
    })
  
    this.dropdown.addEventListener("click", (event) => {
      let target = event.target
      while (target && target.tagName !== "BUTTON") {
        target = target.parentNode
        if (target === this.dropdown) {
          return
        }
      }

      if (target && target.hasAttribute("data-value")) {
        this.selectChoice(target)
      }
    })

    this.dropdown.addEventListener("keydown", (event) => {
      if (event.code === "Escape") {
        this.hideDropdown()
        event.preventDefault()
        event.stopPropagation()
      }

      if (event.code === "ArrowUp") {
        const firstChoice = this.dropdown.querySelector("button")
        if (event.target === firstChoice) {
          if (!this.topChoiceSelected) {
            this.topChoiceSelected = true
          }
        } else {
          this.topChoiceSelected = false
        }
      } else if (event.code === "ArrowDown") {
        this.topChoiceSelected = false
      }
    })

    this.dropdown.addEventListener("keyup", (event) => {
      if (event.code === "ArrowUp" && this.topChoiceSelected) {
        this.topChoiceSelected = false
        this.input.focus()
      }
    })

    document.body.addEventListener("click", (event) => {
      if (this.container !== event.target && !this.container.contains(event.target)) {
        this.hideDropdown()
      }
    })
  }

  createContainer = (input) => {
    const container = document.createElement("div")
    container.classList.add("admin-user-select")

    input.parentNode.insertBefore(container, input)
    container.appendChild(input)
    return container
  }

  createDropdown = () => {
    const dropdown = document.createElement("div")
    dropdown.classList.add("dropdown-menu")
    dropdown.setAttribute("id", (this.options.id || "user-select") + "-dropdown")

    const message = document.createElement("div")
    message.classList.add("admin-user-select-message")
    message.innerText = this.options.initial
    dropdown.appendChild(message)

    this.container.appendChild(dropdown)
    this.container.classList.add("dropdown")

    return dropdown
  }

  createHiddenInput = (name) => {
    const hidden = document.createElement("input")
    hidden.setAttribute("type", "hidden")
    hidden.setAttribute("name", name)
    this.container.appendChild(hidden)
    return hidden
  }

  createChoice = (source) => {
    const choice = document.createElement("div")
    choice.classList.add("form-control")
    choice.classList.add("admin-user-select-with-value")
    choice.innerHTML = source.innerHTML

    this.container.appendChild(choice)
    return choice
  }

  createChoiceClear = () => {
    const button = document.createElement("button")
    button.setAttribute("type", "button")
    button.classList.add("btn")
    button.classList.add("btn-sm")
    button.classList.add("btn-light")
    button.innerText = this.options.clear
  
    this.choice.appendChild(button)
    return button
  }

  setupHtmx = () => {
    const input = this.input
  
    input.setAttribute("name", "search")
    input.setAttribute("hx-get", this.options.api)
    input.setAttribute("hx-trigger", "input changed delay:500ms")
    input.setAttribute("hx-target", "#" + this.dropdown.id)

    htmx.process(this.container)
  }

  showInput = () => {
    this.input.classList.remove("d-none")
  }

  hideInput = () => {
    this.input.classList.add("d-none")
  }

  showDropdown = () => {
    this.container.classList.add("show")
    this.dropdown.classList.add("show")
  }

  hideDropdown = () => {
    this.container.classList.remove("show")
    this.dropdown.classList.remove("show")
  }

  dropdownIsOpen = () => {
    return this.dropdown.classList.contains("show")
  }

  selectChoice = (choice) => {
    clearFieldError(this.input)

    this.hidden.value = choice.getAttribute("data-value")
    this.hideDropdown()
    this.hideInput()

    this.choice = this.createChoice(choice)
    this.clear = this.createChoiceClear()

    this.clear.addEventListener("click", this.clearChoice)
  }

  clearChoice = () => {
    this.clear.remove
    this.clear.remove()
    this.clear = null

    this.choice.remove()
    this.choice = null

    this.showInput()
    this.hidden.value = ""
  }
}

export default function initUserSelect(options) {
  return new UserSelect(options)
}