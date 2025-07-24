const DELAY_DEBOUNCED = 1000
const DELAY_INITIAL = 100

const KEY_CANCEL = {
  Delete: true,
  Space: true,
  MetaLeft: true,
  MetaRight: true,
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
    this.source = config.source
    this.select = config.select

    this.keyCancel = config.keyOverride
      ? Object.assign({}, KEY_CANCEL, config.keyOverride)
      : KEY_CANCEL

    this.getQuery = config.getQuery
    this.onSelect = config.onSelect

    this.delay = {
      debounced: DELAY_DEBOUNCED,
      initial: DELAY_INITIAL,
    }

    if (config.delay) {
      if (typeof config.delay.debounced !== "undefined") {
        this.delay.debounced = config.delay.debounced
      }
      if (typeof config.delay.initial !== "undefined") {
        this.delay.initial = config.delay.initial
      }
    }

    this._debounce = null
    this._query = null

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
    if (this.keyCancel[event.code] && this.select.visible) {
      this.select.handleKey(event.code)
      event.preventDefault()
    } else if (this.keyCancel[event.code]) {
      this.select.hide()
    } else {
      const query = this.getQuery(event.target)

      if (query) {
        this.showSuggestions(query)
      } else {
        this.select.hide()
      }
    }
  }

  showSuggestions = (query) => {
    if (query.text === this._query.text) {
      return
    }

    if (!!this._debounce) {
      window.clearTimeout(this._debounce)
      this._debounce = null
    }

    this._query = query
    this._debounce = window.setTimeout(
      () => {
        this.source.get(query.text).then((results) => {})
      },
      this._debounce ? this.delay.debounced : this.delay.initial
    )
  }
}

export default Autocomplete
