import "bootstrap/js/transition"
import "bootstrap/js/affix"
import "bootstrap/js/modal"
import "bootstrap/js/dropdown"
import "at-js"
import "cropit"
import "jquery-caret"
import htmx from "htmx.org"
import OrderedList from "misago/utils/ordered-list"
import "misago/style/index.less"
import AjaxLoader, { useLoader } from "./AjaxLoader"
import BulkModeration from "./BulkModeration"
import { Mention } from "./Autocomplete"
import { deleteElement, slideUpElement } from "./animations"
import "./focusOn"
import "./formValidators"
import "./htmxErrors"
import "./htmxExtensionLoaderTpl"
import Lightbox from "./lightbox"
import editor, { activateEditors } from "./editor"
import "./pagination"
import activatePollChoicesControl from "./PollChoicesControl"
import quote from "./Quote"
import "./richtext"
import * as snackbars from "./snackbars"
import { updateTabGroups } from "./TabGroups"
import userMultipleChoice from "./UserMultipleChoice"
import "./scrollTo"
import "./timestamps"

const loader = new AjaxLoader()
const lightbox = new Lightbox()

htmx.config.historyEnabled = false
htmx.config.historyCacheSize = 0

export class Misago {
  constructor() {
    this._initializers = []
    this._context = {}

    this.htmx = htmx

    this.loader = loader
    this.editor = editor
    this.lightbox = lightbox
    this.quote = quote

    this.deleteElement = deleteElement
    this.slideUpElement = slideUpElement

    this.activatePollChoicesControl = activatePollChoicesControl
    this.tabGroups = updateTabGroups
    this.userMultipleChoice = userMultipleChoice
  }

  addInitializer(initializer) {
    this._initializers.push({
      key: initializer.name,

      item: initializer.initializer,

      after: initializer.after,
      before: initializer.before,
    })
  }

  init(context) {
    this._context = context

    var initOrder = new OrderedList(this._initializers).orderedValues()
    initOrder.forEach((initializer) => {
      initializer(this)
    })
  }

  // context accessors
  has(key) {
    return !!this._context[key]
  }

  get(key, fallback) {
    if (this.has(key)) {
      return this._context[key]
    } else {
      return fallback || undefined
    }
  }

  pop(key) {
    if (this.has(key)) {
      let value = this._context[key]
      this._context[key] = null
      return value
    } else {
      return undefined
    }
  }

  snackbar(type, message) {
    snackbars.snackbar(type, message)
  }

  snackbarInfo(message) {
    snackbars.info(message)
  }

  snackbarSuccess(message) {
    snackbars.success(message)
  }

  snackbarWarning(message) {
    snackbars.warning(message)
  }

  snackbarError(message) {
    snackbars.error(message)
  }

  snackbarHttpResponseError(response) {
    snackbars.httpResponseError(response)
  }

  bulkModeration(options) {
    return new BulkModeration(options)
  }

  hideMarkAsReadModal = () => {
    $("#mark-as-read").modal("hide")
  }

  mention = (control) => {
    return new Mention(control)
  }
}

// create the singleton
const misago = new Misago()

// expose it globally
window.misago = misago

// and export it for tests and stuff
export default misago

// Register ajax loader events
document.addEventListener("htmx:beforeRequest", ({ target }) => {
  if (useLoader(target)) {
    loader.show()
  }
})

document.addEventListener("htmx:afterRequest", ({ target }) => {
  if (useLoader(target)) {
    loader.hide()
  }
})

// Register editor events
document.addEventListener("htmx:load", activateEditors)

// Hide moderation modal
document.addEventListener("misago:afterModeration", () => {
  $("#threads-moderation-modal").modal("hide")
})

document.addEventListener("misago:afterUpdateMembers", () => {
  $("#add-members-modal").modal("hide")
})

// Custom misago-confirm attribute
document.addEventListener("submit", function (event) {
  const element = event.target.closest("form[misago-confirm]")
  if (!!element && !window.confirm(element.getAttribute("misago-confirm"))) {
    event.preventDefault()
  }
})
