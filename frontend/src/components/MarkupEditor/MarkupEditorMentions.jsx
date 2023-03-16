import React from "react"

const SELECT_EVENTS = ["focus", "mouseup", "touchend"]
const SCAN_RANGE = 50
const ALPHANUMERIC = /^[\p{sc=Latn}\p{Nd}]$/u
const NON_ALPHANUMERIC = /[^\p{sc=Latn}\p{Nd}]/u

const DEBOUNCING = 800

const CACHE = {}

export default class MarkupEditorMentions extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      mention: null,
      open: false,
      query: null,
      choices: [],
      choice: -1,
    }

    this.element = null
    this.phantom = null
    this.fetch = null
  }

  componentDidMount = () => {
    if (!this.element) return

    window.setTimeout(() => {
      const textarea = this.element.firstChild
      SELECT_EVENTS.forEach((event) => {
        textarea.addEventListener(event, this.handleSelect)
      })
      
      textarea.addEventListener("keydown", this.handleKeyDown)

      this.phantom = createPhantomElement(textarea)
    }, 500)
  }

  componentWillUnmount = () => {
    if (this.element.firstChild) {
      const textarea = this.element.firstChild
      SELECT_EVENTS.forEach((event) => {
        textarea.removeEventListener(event, this.handleSelect)
      })
      
      textarea.removeEventListener("keydown", this.handleKeyDown)
    }

    if (this.phantom) {
      document.body.removeChild(this.phantom)
      this.phantom = null
    }

    if (this.fetch) {
      window.clearTimeout(this.fetch)
      this.fetch = null
    }
  }

  handleSelect = (event) => {
    const mention = getMentionState(event.target, this.props.value)
    const position = getMentionPosition(
      this.element.firstChild,
      this.phantom,
      this.props.value,
      mention
    )

    this.setState({
      mention,
      position,
      choices: [],
      choice: -1,
      open: !!mention && !!position,
      query: !!mention ? mention.prefix : null,
    })

    if (!!mention) {
      this.fetchSuggestions(mention.prefix)
    }
  }

  handleKeyDown = (event) => {
    /* TODO
    If UI is open and component is not disabled, up/down/esc/enter keys
    channge function:

    up - decrease choice
    down - increase choice
    enter - insert choice
    escape - close UI
    */
    console.log("TODO!")
  }

  fetchSuggestions = (query) => {
    if (CACHE[query]) {
      this.setState({
        choices: CACHE[query],
        choice: -1,
      })
      return
    }

    if (this.fetch) {
      window.clearTimeout(this.fetch)
      this.fetch = null
    }

    this.fetch = window.setTimeout(() => {
      $.getJSON(misago.get("MENTION_API"), { q: query }, (data) => {
        CACHE[query] = data

        this.setState({
          choices: CACHE[query],
          choice: -1,
        })
      })
    }, DEBOUNCING)
  }

  insertMention = (username) => {
    if (this.state.mention) {
      const { start, end } = this.state.mention
      const textarea = this.element.firstChild
      const caret = start + username.length

      this.props.update(
        this.props.value.substr(0, start) +
          username +
          this.props.value.substr(end)
      )

      textarea.setSelectionRange(caret, caret)
      textarea.focus()

      this.setState({ open: false })
    }
  }

  render = () => {
    return (
      <div
        className="markup-editor-state.mentions-container"
        style={{ position: "relative" }}
        ref={(element) => {
          if (element) {
            this.element = element
          }
        }}
      >
        {this.props.children}
        {this.state.open && !this.props.disabled && (
          <div
            style={{
              position: "absolute",
              top: this.state.position.top,
              left: this.state.position.left,
              background: "#fff",
              border: "1px solid #ccc",
              boxShadow: "0px 0px 3px #999",
              maxWidth: "150px",
            }}
          >
            {this.state.choices.map(({ avatar, username }, index) => (
              <button
                style={{
                  display: "block",
                  border: "none",
                  background: "#fff",
                  color: "#000",
                  textAlign: "left",
                  padding: "8px 12px",
                  width: "100%",
                }}
                key={this.state.query + index}
                type="button"
                onClick={() => this.insertMention(username)}
              >
                <img src={avatar} width="16" height="16" />{" "}
                <strong>{username.substr(0, this.state.mention.caret)}</strong>
                {username.substr(this.state.mention.caret)}
              </button>
            ))}
          </div>
        )}
      </div>
    )
  }
}

function getMentionState(textarea, value) {
  if (textarea.disabled) {
    return null // Skip disabled input
  }

  if (textarea.selectionStart != textarea.selectionEnd) {
    return null // Skip text block or first character
  }

  const caret = textarea.selectionStart
  if (caret === 0) {
    return null // Skip text start
  }

  const mention = getMentionData(caret, value)
  if (mention === null) {
    return null // Skip text without mention
  }

  return mention
}

function getMentionData(caret, value) {
  const start = value.substr(0, caret).lastIndexOf("@")
  if (start === -1) {
    return null // Mention start sign not found
  }

  if (start > 0 && value.substr(start - 1, 1).match(ALPHANUMERIC)) {
    return null // Mention can't be prefixed by alpha-numeric sign
  }

  const end = value.substr(start + 1, SCAN_RANGE).search(NON_ALPHANUMERIC)
  if (end !== -1 && start + 1 + end < caret) {
    return null // Caret is after mention's end
  }

  const mention =
    end === -1 ? value.substr(start + 1) : value.substr(start + 1, end)

  if (mention.length === 0) {
    return null // Empty mention string
  }

  const prefix = caret - start - 1
  if (prefix === 0) {
    return null // Caret is before first character of mention
  }

  return {
    start: start + 1,
    end: start + 1 + mention.length,
    caret: prefix,
    prefix: mention.substr(0, prefix),
    suffix: mention.substr(prefix),
    mention,
  }
}

function createPhantomElement(source) {
  const sourceStyles = window.getComputedStyle(source, null)
  const phantom = document.createElement("div")

  phantom.ariaHidden = "true"

  phantom.style.position = "absolute"
  phantom.style.top = window.innerHeight * -2
  phantom.style.left = window.innerWidth * -2

  phantom.style.fontFamily = sourceStyles.fontFamily
  phantom.style.fontSize = sourceStyles.fontSize
  phantom.style.fontWeight = sourceStyles.fontWeight
  phantom.style.lineHeight = sourceStyles.lineHeight
  phantom.style.padding = sourceStyles.padding
  phantom.style.maxWidth = sourceStyles.width

  document.body.appendChild(phantom)
  return phantom
}

function getMentionPosition(textarea, phantom, value, mention) {
  if (mention === null) {
    return null // Position not needed
  }

  const style = window.getComputedStyle(textarea)
  const prefix = value.substr(0, mention.start)

  const topOffset = parseInt(style.paddingBottom)
  const rightOffset = parseInt(style.paddingRight)

  if (prefix.indexOf("\n") === -1) {
    phantom.innerText = prefix
    const top = phantom.clientHeight - topOffset
    const left = phantom.clientWidth - rightOffset

    phantom.innerText = ""
    return { top, left }
  }

  phantom.innerText = prefix
  const top = phantom.clientHeight - topOffset

  phantom.innerText = prefix.substr(prefix.lastIndexOf("\n") + 1)
  const left = phantom.clientWidth - rightOffset

  phantom.innerText = ""
  return { top, left }
}
