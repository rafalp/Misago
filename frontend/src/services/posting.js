import React from "react"
import PostingComponent from "../components/posting"
import renderComponent from "../utils/renderComponent"

export class Posting {
  init(ajax, snackbar, element, root) {
    this._ajax = ajax
    this._snackbar = snackbar
    this._element = element
    this._root = root

    this._mode = null
    this._spacer = document.getElementById("posting-spacer")
    this._observer = new ResizeObserver((entries) => {
      this._spacer.style.height = entries[0].contentRect.height + "px"
    })

    this._isOpen = false
    this._isClosing = false

    this._beforeunloadSet = false
  }

  isOpen() {
    return this._isOpen
  }

  setBeforeUnload() {
    if (!this._beforeunloadSet) {
      window.addEventListener("beforeunload", this.beforeUnload, { capture: true })
      this._beforeunloadSet = true
    }
  }

  unsetBeforeUnload() {
    window.removeEventListener("beforeunload", this.beforeUnload, { capture: true })
    this._beforeunloadSet = false
  }

  beforeUnload(event) {
    event.returnValue = "true"
    return "true"
  }

  open(props) {
    if (this._isOpen === false) {
      this._mode = props.mode
      this._isOpen = props.submit
      this._realOpen(props)
    } else if (this._isOpen !== props.submit) {
      let message = gettext(
        "You are already working on other message. Do you want to discard it?"
      )

      const changeForm = window.confirm(message)
      if (changeForm) {
        this._mode = props.mode
        this._isOpen = props.submit
        this._realOpen(props)
      }
    } else if (this._mode == "REPLY" && props.mode == "REPLY") {
      this._realOpen(props)
    }
  }

  _realOpen(props) {
    renderComponent(<PostingComponent {...props} />, this._root)
    this._element.classList.add("show")
    this._observer.observe(this._element)
    this.setBeforeUnload()
  }

  close = () => {
    this.unsetBeforeUnload()

    if (this._isOpen && !this._isClosing) {
      this._isClosing = true
      this._element.classList.remove("show")

      window.setTimeout(() => {
        this._root.unmount()
        this._observer.unobserve(this._element)
        this._spacer.style.height = "0px;"
        this._isClosing = false
        this._isOpen = false
        this._mode = null
      }, 300)
    }
  }
}

export default new Posting()
