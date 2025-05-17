import { computePosition, flip, offset, shift } from "@floating-ui/dom"

class Select {
  constructor() {
    this.element = document.createElement("div")
    this.element.classList.add("autocomplete-user-popup")
    document.body.appendChild(this.element)

    this.shadow = document.createElement("pre")
    this.shadow.ariaHidden = true
    this.shadow.style.position = "absolute"
    this.shadow.style.top = 0
    this.shadow.style.left = "-9999px"
    this.shadow.style.opacity = 0
    this.shadow.style.zIndex = -999
    document.body.appendChild(this.shadow)

    this.choice = 0
    this.choices = []
    this.maxChoice = 0
    this.callback = null

    this.visible = false

    document.body.addEventListener("click", (event) => {
      if (this.visible && !this.element.contains(event.target)) {
        this.hide()
      }
    })
  }

  updateChoices(target, query, choices, callback) {
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

      // element.innerHTML = choice.username
      element.addEventListener("click", () => {
        callback(choice.username)
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

  getTextPosition = (target, query) => {
    this.shadow.innerHTML = target.value.substring(0, query.end - 1)
    this.shadow.setAttribute("class", target.getAttribute("class"))

    const targetRect = target.getBoundingClientRect()
    this.shadow.style.width = `${targetRect.width}px`
    this.shadow.style.height = `${targetRect.height}px`

    const marker = document.createElement("span")
    marker.innerHTML = query.text.substring(query.text.length - 1)
    this.shadow.appendChild(marker)

    const shadowRect = this.shadow.getBoundingClientRect()
    const markerRect = marker.getBoundingClientRect()

    const rect = {
      bottom:
        targetRect.bottom -
        markerRect.bottom -
        shadowRect.bottom +
        target.scrollTop,
      height: markerRect.height,
      left: targetRect.left + markerRect.left - shadowRect.left,
      right: targetRect.right - markerRect.right - shadowRect.right,
      top: targetRect.top + markerRect.top - shadowRect.top - target.scrollTop,
      width: markerRect.width,
      x: targetRect.x + markerRect.x - shadowRect.x,
      y: targetRect.y + markerRect.y - shadowRect.y,
    }

    return {
      getBoundingClientRect() {
        return rect
      },
    }
  }

  handleKey = (keyCode) => {
    if (keyCode === "Enter") {
      this.callback(this.choices[this.choice])
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

  show = (target, query, choices, callback) => {
    if (choices.length === 0) {
      this.hide()
    } else {
      this.updateChoices(target, query, choices, callback)
      this.element.classList.add("show")

      const textPosition = this.getTextPosition(target, query)

      computePosition(textPosition, this.element, {
        placement: "top",
        middleware: [offset(6), flip(), shift({ padding: 8 })],
      }).then(({ x, y }) => {
        Object.assign(this.element.style, {
          left: `${x}px`,
          top: `${y}px`,
        })
      })

      this.choices = choices.map(({ username }) => username)
      this.choice = 0
      this.maxChoice = choices.length - 1
      this.callback = callback

      this.visible = true
    }
  }

  hide = () => {
    this.element.classList.remove("show")
    this.visible = false
  }
}

const select = new Select()

export default select
