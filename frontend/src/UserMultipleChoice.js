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
      const text = control.value.trim().replace(/\s+/, "")
      return { prefix: "", text }
    }

    const onSelect = (choice) => {
      const item = this.template.content.cloneNode(true)

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
      this.input.before(item)
    }

    this.autocomplete = new Autocomplete({
      control: this.input,
      keyOverride: KEY_OVERRIDE,
      source: sources.users,
      select: new SelectUser({
        anchor: new AnchorInput(this.input),
      }),
      getQuery,
      onSelect,
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
