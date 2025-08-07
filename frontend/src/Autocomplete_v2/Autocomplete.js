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
    this.anchor = config.anchor
    this.source = config.source
    this.getQuery = config.getQuery
    this.select = config.select
    this.errors = config.errors || true

    this.keyCancel = config.keyOverride
      ? Object.assign({}, KEY_CANCEL, config.keyOverride)
      : KEY_CANCEL

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

    this.control.addEventListener("keydown", this.onKeyDown)
    this.control.addEventListener("keyup", this.onKeyUp)
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
    if (!query.value.trim()) {
      return
    }

    if (!!this._debounce) {
      window.clearTimeout(this._debounce)
      this._debounce = null
    }

    this._debounce = window.setTimeout(
      () => {
        this.source(query, this.errors)
          .then((data) => {
            if (this.select && this.onSelect) {
              this.select.show(query, data, this.onSelect)
            } else {
              console.warn(
                "Autocomplete was initialized without the 'select' or 'onSelect' options."
              )
            }
          })
          .then(() => {
            this._debounce = null
          })
      },
      this._debounce ? this.delay.debounced : this.delay.initial
    )
  }

  isEventTarget = (event) => {
    return this.select.isEventTarget(event)
  }
}

export default Autocomplete
