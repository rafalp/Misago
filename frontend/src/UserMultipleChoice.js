import htmx from "htmx.org"
import {
  Autocomplete,
  AnchorInput,
  SelectUser,
  sources,
} from "./Autocomplete_v2"

const DATA_ATTRIBUTE_ELEMENT = "m-user-multiple-choice"
const DATA_ATTRIBUTE_INPUT = "m-user-multiple-choice-input"

const SELECTOR_ELEMENT = `[${DATA_ATTRIBUTE_ELEMENT}]`
const SELECTOR_INPUT = `[${DATA_ATTRIBUTE_INPUT}]`

const TEMPLATE_ID = "m-user-multiple-choice-template"

const CLASS_NAME_FOCUS = "focused"

const EVENT_FOCUS = ["focusin", "click"]

const KEY_OVERRIDE = {
  Delete: false,
  Space: false,
  ArrowLeft: false,
  ArrowRight: false,
}

class UserMultipleChoice {
  constructor() {
    this.autocomplete = null
    this.element = null
    this.input = null
    this.template = null
  }

  activate = (element) => {
    if (element.getAttribute(DATA_ATTRIBUTE_ELEMENT) === "true") {
      return
    }

    element.setAttribute(DATA_ATTRIBUTE_ELEMENT, "true")

    this.element = element
    this.input = document.querySelector(SELECTOR_INPUT)
    this.template = document.getElementById(TEMPLATE_ID)

    function getQuery(control) {
      const value = control.value.trim().replace(/\s+/, "")
      if (value.length) {
        const exclude = []
        element.querySelectorAll("[m-user-id]").forEach(function (item) {
          exclude.push(item.getAttribute("m-user-id"))
        })
        return { prefix: "", exclude, value }
      }
      return null
    }

    const onSelect = (choice) => {
      const item = this.template.content.cloneNode(true)

      item.querySelector("li").setAttribute("m-user-id", choice.id)
      item.querySelector("input").value = choice.slug
      item.querySelector('slot[name="username"]').replaceWith(choice.username)

      const avatars = choice.avatar
        .filter(function ({ size }) {
          return size >= 32
        })
        .reverse()

      const img = item.querySelector("img")
      if (avatars.length) {
        img.setAttribute("src", avatars[0].url)
      } else {
        img.remove()
      }

      this.input.value = ""
      this.input.parentElement.before(item)
      this.input.focus()

      this.focus()
    }

    this.autocomplete = new Autocomplete({
      control: this.input,
      keyOverride: KEY_OVERRIDE,
      source: sources.users,
      select: new SelectUser({
        anchor: new AnchorInput(this.input),
        placement: "bottom-start",
      }),
      getQuery,
      onSelect,
    })

    EVENT_FOCUS.forEach((eventName) => {
      element.addEventListener(eventName, this.focus)
    })

    EVENT_FOCUS.forEach((eventName) => {
      document.addEventListener(eventName, (event) => {
        if (
          !element.contains(event.target) &&
          !this.autocomplete.isEventTarget(event)
        ) {
          this.blur()
        }
      })
    })

    this.element.addEventListener("click", (event) => {
      const button = event.target.closest("button")
      if (button) {
        button.closest("li").remove()
      }

      this.focus()
    })

    let backspacePressed = false

    this.input.addEventListener("keydown", function (event) {
      if (event.key === "Backspace") {
        if (!backspacePressed) {
          backspacePressed = true
          if (event.target.value.trim() === "") {
            const lastItem = event.target.closest("li").previousElementSibling
            if (lastItem) {
              lastItem.remove()
            }
          }
        }
      }
    })

    this.input.addEventListener("keyup", function (event) {
      if (event.key === "Backspace") {
        backspacePressed = false
      }
    })
  }

  focus = () => {
    this.element.classList.add(CLASS_NAME_FOCUS)
  }

  blur = () => {
    this.element.classList.remove(CLASS_NAME_FOCUS)
  }
}

const singleton = new UserMultipleChoice()

htmx.onLoad(function () {
  const element = document.querySelector(SELECTOR_ELEMENT)
  if (element) {
    singleton.activate(element)
  }
})

export default singleton

export { UserMultipleChoice }
