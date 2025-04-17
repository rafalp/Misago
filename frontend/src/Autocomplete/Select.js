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
    this.shadow.style.left = -9999
    this.shadow.style.opacity = 0
    this.shadow.style.zIndex = -999
    document.body.appendChild(this.shadow)

    this.target = null
    this.visible = false

    document.body.addEventListener("click", (event) => {
      if (this.visible && !this.element.contains(event.target)) {
        this.hide()
      }
    })
  }

  update(target, query, choices, callback) {
    const children = choices.map((choice) => {
      const element = document.createElement("button")
      element.setAttribute("type", "button")
      element.classList.add("autocomplete-user-popup-choice")

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

    console.log(targetRect)
    console.log(shadowRect)
    console.log(markerRect)

    const rect = {
      bottom: targetRect.bottom - markerRect.bottom - shadowRect.bottom,
      height: markerRect.height,
      left: targetRect.left + markerRect.left - shadowRect.left,
      right: targetRect.right - markerRect.right - shadowRect.right,
      top: targetRect.top + markerRect.top - shadowRect.top,
      width: markerRect.width,
      x: targetRect.x + markerRect.x - shadowRect.x,
      y: targetRect.y + markerRect.y - shadowRect.y,
    }

    console.log(rect)

    return {
      getBoundingClientRect() {
        return rect
      },
    }
  }

  show = (target, query, choices, callback) => {
    if (choices.length === 0) {
      this.hide()
    } else {
      this.update(target, query, choices, callback)
      this.element.classList.add("show")

      const textPosition = this.getTextPosition(target, query)

      computePosition(textPosition, this.element, {
        placement: "top",
        middleware: [offset(8), flip(), shift({ padding: 8 })],
      }).then(({ x, y }) => {
        Object.assign(this.element.style, {
          left: `${x}px`,
          top: `${y}px`,
        })
      })

      this.target = target
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
