const KEY_INVALID = {
  Delete: true,
  Space: true,
  MetaLeft: true,
  End: true,
  Enter: true,
  ArrowUp: true,
  ArrowDown: true,
  ArrowLeft: true,
  ArrowRight: true,
}

const KEY_SELECT = {
  Escape: true,
  Enter: true,
  ArrowUp: true,
  ArrowDown: true,
}

class Autocomplete {
  constructor(config) {
    this.control = config.control
    this.select = config.select

    this.getQuery = config.getQuery
    this.onSelect = config.onSelect

    this.control.addEventListener("keydown", this.onKeyDown)
    this.control.addEventListener("keyup", this.onKeyUp)
    this.control.addEventListener("blur", this.select.hide)
  }

  onKeyDown = (event) => {
    if (KEY_SELECT[event.code] && this.select.visible) {
      event.preventDefault()
    }
  }

  onKeyUp = (event) => {
    if (KEY_INVALID[event.code] && this.select.visible) {
      this.select.handleKey(event.code)
      event.preventDefault()
    } else if (KEY_INVALID[event.code]) {
      this.select.hide()
    } else {
      const query = this.getQuery(event.target)

      if (query) {
        // this.getSuggestions(query)
      } else {
        this.select.hide()
      }
    }
  }
}

export default Autocomplete
