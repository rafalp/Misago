import React from "react"
import ReactDOM from "react-dom"
import PostingComponent from "misago/components/posting"
import mount from "misago/utils/mount-component"

export class Posting {
  init(ajax, snackbar, mount) {
    this._ajax = ajax
    this._snackbar = snackbar
    this._mount = mount

    this._mode = null
    this._spacer = document.getElementById("posting-spacer")
    this._observer = new ResizeObserver((entries) => {
      this._spacer.style.height = entries[0].contentRect.height + "px"
    })

    this._isOpen = false
    this._isClosing = false

    this._beforeunloadSet = false
    this._props = null
  }

  isOpen() {
    return this._isOpen
  }

  setBeforeUnload() {
    if (!this._beforeunloadSet) {
      window.addEventListener("beforeunload", this.beforeUnload, {
        capture: true,
      })
      this._beforeunloadSet = true
    }
  }

  unsetBeforeUnload() {
    window.removeEventListener("beforeunload", this.beforeUnload, {
      capture: true,
    })
    this._beforeunloadSet = false
  }

  beforeUnload(event) {
    event.returnValue = "true"
    return "true"
  }

  open(props) {
    if (this._isOpen === false) {
      if (props.mode === "QUOTE") {
        this._mode = "REPLY"
      } else {
        this._mode = props.mode
      }

      this._isOpen = props.submit
      this._realOpen(Object.assign({}, props, { mode: this._mode }))
    } else if (props.mode === "QUOTE") {
      this._realOpen(
        Object.assign({}, this._props, {
          config: props.config,
          context: props.context,
        })
      )
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
    mount(<PostingComponent {...props} />, this._mount.id)

    this._props = props
    this._mount.classList.add("show")
    this._observer.observe(this._mount)
    this.setBeforeUnload()
  }

  close = () => {
    this.unsetBeforeUnload()
    this._props = null

    if (this._isOpen && !this._isClosing) {
      this._isClosing = true
      this._mount.classList.remove("show")

      window.setTimeout(() => {
        ReactDOM.unmountComponentAtNode(this._mount)
        this._observer.unobserve(this._mount)
        this._spacer.style.height = "0px;"
        this._isClosing = false
        this._isOpen = false
        this._mode = null
      }, 300)
    }
  }
}

export default new Posting()
