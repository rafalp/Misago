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
  constructor(options) {
    this.control = options.control
    this.select = options.select

    this.getQuery = options.getQuery
    this.onSelect = options.onSelect

    control.addEventListener("keydown", this.onKeyDown)
    control.addEventListener("keyup", this.onKeyUp)
    control.addEventListener("blur", select.hide)
  }

  onKeyDown = (event) => {
    if (KEY_SELECT[event.code] && select.visible) {
      event.preventDefault()
    }
  }

  onKeyUp = (event) => {
    if (KEY_INVALID[event.code] && select.visible) {
      select.handleKey(event.code)
      event.preventDefault()
    } else if (INVALID_KEYS[event.code]) {
      select.hide()
    } else {
      const query = this.getQuery(event.target)

      if (query) {
        this.getSuggestions(query)
      } else {
        select.hide()
      }
    }
  }
}

export default Autocomplete
