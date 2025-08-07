import { computePosition, flip, offset, shift } from "@floating-ui/dom"

class SelectUser {
  constructor(config) {
    this.element = document.createElement("div")
    this.element.classList.add("autocomplete-user-popup")
    document.body.appendChild(this.element)

    this.anchor = config.anchor
    this.placement = config.placement || "bottom"
    this.offset = config.offset || 6
    this.shift = config.shift || { padding: 8 }

    this.choice = 0
    this.choices = []
    this.maxChoice = 0

    this.query = null
    this.callback = null

    this.visible = false

    document.body.addEventListener("click", (event) => {
      if (this.visible && !this.element.contains(event.target)) {
        this.hide()
      }
    })
  }

  updateChoices(query, choices, callback) {
    const children = choices.map((choice, index) => {
      const element = document.createElement("button")
      element.setAttribute("type", "button")
      element.classList.add("autocomplete-user-popup-choice")

      if (index === 0) {
        element.classList.add("active")
      }

      const avatars = choice.avatar.filter(({ size }) => size >= 24)
      const avatarsHd = choice.avatar.filter(({ size }) => size >= 48)

      const img = document.createElement("img")
      img.classList.add("autocomplete-user-popup-choice-avatar")
      img.setAttribute("src", avatars[avatars.length - 1].url)
      img.setAttribute("srcset", avatarsHd[avatarsHd.length - 1].url)
      img.setAttribute("alt", "")
      element.appendChild(img)

      const span = document.createElement("span")
      span.classList.add("autocomplete-user-popup-choice-username")
      span.innerText = choice.username
      element.appendChild(span)

      element.addEventListener("click", () => {
        callback(choice, query)
        this.hide()
      })
      return element
    })

    this.element.replaceChildren(...children)
  }

  updateActiveChoice() {
    for (let index = 0; index < this.element.children.length; index++) {
      const choice = this.element.children[index]
      if (index === this.choice) {
        choice.classList.add("active")
      } else {
        choice.classList.remove("active")
      }
    }
  }

  handleKey = (keyCode) => {
    if (keyCode === "Enter") {
      this.callback(this.choices[this.choice], this.query)
      this.hide()
    } else if (keyCode === "ArrowUp") {
      if (this.choice > 0) {
        this.choice--
      } else {
        this.choice = this.maxChoice
      }
      this.updateActiveChoice()
    } else if (keyCode === "ArrowDown") {
      if (this.choice < this.maxChoice) {
        this.choice++
      } else {
        this.choice = 0
      }
      this.updateActiveChoice()
    } else if (keyCode === "Escape") {
      this.hide()
    }
  }

  isEventTarget = (event) => {
    if (event.relatedTarget) {
      return !!this.element.contains(event.relatedTarget)
    } else if (event.target) {
      return !!this.element.contains(event.target)
    } else {
      return false
    }
  }

  show = (query, choices, callback) => {
    if (choices.length === 0) {
      this.hide()
    } else {
      this.updateChoices(query, choices, callback)
      this.element.classList.add("show")

      const target = this.anchor.getTarget(query)

      computePosition(target, this.element, {
        placement: this.placement,
        middleware: [offset(this.offset), flip(), shift(this.shift)],
      }).then(({ x, y }) => {
        Object.assign(this.element.style, {
          left: `${x}px`,
          top: `${y}px`,
        })
      })

      this.choices = choices
      this.choice = 0
      this.maxChoice = choices.length - 1

      this.query = query
      this.callback = callback

      this.visible = true
    }
  }

  hide = () => {
    this.element.classList.remove("show")
    this.visible = false
  }
}

export default SelectUser
