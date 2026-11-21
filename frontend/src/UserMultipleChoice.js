import htmx from "htmx.org"
import { Autocomplete, AnchorInput, SelectUser, sources } from "./Autocomplete"

const ATTRIBUTE_ACTIVE = "m-user-multiple-choice-active"
const ATTRIBUTE_CHIPS = "m-user-multiple-choice"
const ATTRIBUTE_SEARCH = "m-user-multiple-choice-search"
const ATTRIBUTE_USER_ID = "m-user-id"
const ATTRIBUTE_USER_NAME = "m-user-name"

const SELECTOR_CHIPS = `[${ATTRIBUTE_CHIPS}]`
const SELECTOR_SEARCH = `[${ATTRIBUTE_SEARCH}]`
const SELECTOR_USER_ID = `[${ATTRIBUTE_USER_ID}]`
const SELECTOR_USER_NAME = `[${ATTRIBUTE_USER_NAME}]`

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
    this.input = null
    this.chips = null
    this.search = null
    this.template = null
  }

  activate = (chips) => {
    if (chips.getAttribute(ATTRIBUTE_ACTIVE)) {
      return
    } else {
      chips.setAttribute(ATTRIBUTE_ACTIVE, "true")
    }

    const inputId = chips.getAttribute(ATTRIBUTE_CHIPS)

    if (!inputId) {
      console.warn(
        `${SELECTOR_CHIPS} attribute must be an ID of input element.`
      )
      return
    }

    this.input = document.getElementById(inputId)
    if (!this.input) {
      console.warn(`Element with id="${inputId}" doesn't exist.`)
      return
    }

    this.input.type = "hidden"

    this.chips = chips
    this.maxChoices = Number(chips.getAttribute("maxchoices") || 1)
    this.search = document.querySelector(SELECTOR_SEARCH)
    this.template = document.getElementById(TEMPLATE_ID)

    this.input.removeAttribute("id")
    this.search.setAttribute("id", inputId)

    this.updateSearchDisabled()

    function getQuery(control) {
      const value = control.value.trim().replace(/\s+/, "")
      if (value.length) {
        const exclude = []
        chips.querySelectorAll(SELECTOR_USER_ID).forEach(function (item) {
          exclude.push(item.getAttribute(ATTRIBUTE_USER_ID))
        })
        return { exclude, value }
      }
      return null
    }

    const onSelect = (choice) => {
      const item = this.template.content.cloneNode(true)

      item.querySelector("li").setAttribute(ATTRIBUTE_USER_ID, choice.id)
      item
        .querySelector("li")
        .setAttribute(ATTRIBUTE_USER_NAME, choice.username)
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

      this.search.value = ""
      this.search.parentElement.before(item)

      this.updateInputValue()
      this.updateSearchDisabled()

      if (!this.search.disabled) {
        this.search.focus()
      }

      this.focus()
    }

    this.autocomplete = new Autocomplete({
      control: this.search,
      keyOverride: KEY_OVERRIDE,
      source: sources.users,
      select: new SelectUser({
        anchor: new AnchorInput(this.search),
        placement: "bottom-start",
      }),
      getQuery,
      onSelect,
    })

    EVENT_FOCUS.forEach((eventName) => {
      chips.addEventListener(eventName, this.focus)
    })

    EVENT_FOCUS.forEach((eventName) => {
      document.addEventListener(eventName, (event) => {
        if (
          !chips.contains(event.target) &&
          !this.autocomplete.isEventTarget(event)
        ) {
          this.blur()
        }
      })
    })

    this.chips.addEventListener("click", (event) => {
      const button = event.target.closest("button")
      if (button) {
        this.deleteItem(button.closest("li"))
      }
      this.focus()
    })

    let backspacePressed = false

    this.search.addEventListener("keydown", (event) => {
      if (event.key === "Backspace") {
        if (!backspacePressed) {
          backspacePressed = true
          if (event.target.value.trim() === "") {
            const lastItem = event.target.closest("li").previousElementSibling
            if (lastItem) {
              this.deleteItem(lastItem)
            }
          }
        }
      }
    })

    this.search.addEventListener("keyup", function (event) {
      if (event.key === "Backspace") {
        backspacePressed = false
      }
    })
  }

  focus = () => {
    this.chips.classList.add(CLASS_NAME_FOCUS)
  }

  blur = () => {
    this.chips.classList.remove(CLASS_NAME_FOCUS)
  }

  deleteItem = (element) => {
    element.remove()
    this.updateSearchDisabled()
    this.updateInputValue()
  }

  updateSearchDisabled = () => {
    this.search.disabled =
      this.chips.querySelectorAll("li").length - 1 >= this.maxChoices
  }

  updateInputValue = () => {
    const usernames = []
    this.chips.querySelectorAll(SELECTOR_USER_NAME).forEach((chip) => {
      usernames.push(chip.getAttribute(ATTRIBUTE_USER_NAME))
    })
    this.input.value = usernames.join(", ")
  }
}

const singleton = new UserMultipleChoice()

htmx.onLoad(function () {
  const chips = document.querySelector(SELECTOR_CHIPS)
  if (chips) {
    singleton.activate(chips)
  }
})

export default singleton

export { UserMultipleChoice }
