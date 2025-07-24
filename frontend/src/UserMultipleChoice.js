import htmx from "htmx.org"
import { Autocomplete, getUsers } from "./Autocomplete"

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

    this.autocomplete = new Autocomplete({
      control: this.input,
      keyOverride: KEY_OVERRIDE,
      source: getUsers,
      select: {
        hide: () => console.log("hide select"),
      },
      getQuery: (control) => control.value.trim().replace(/\s+/, ""),
      onSelect: null,
    })

    EVENT_FOCUS.forEach((event) => {
      element.addEventListener(event, this.onFocus)
    })

    EVENT_FOCUS.forEach((event) => {
      document.addEventListener(event, (event) => {
        if (!element.contains(event.target)) {
          this.onBlur()
        }
      })
    })
  }

  onFocus = () => {
    this.element.classList.add(CLASS_NAME_FOCUS)
  }

  onBlur = () => {
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
