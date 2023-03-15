import React from "react"

const EVENTS = ["keyup", "focus", "mouseup", "touchend"]
const SCAN_RANGE = 50
const ALPHANUMERIC = /^[\p{sc=Latn}\p{Nd}]$/u
const NON_ALPHANUMERIC = /[^\p{sc=Latn}\p{Nd}]/u

export default class MarkupEditorMention extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      mention: null,
    }

    this.element = null
    this.phantom = null
  }

  componentDidMount = () => {
    if (!this.element) return

    window.setTimeout(() => {
      const textarea = this.element.firstChild
      EVENTS.forEach((event) => {
        textarea.addEventListener(event, this.eventHandler)
      })

      this.phantom = createPhantomElement(textarea)
    }, 500)
  }

  componentWillUnmount = () => {
    if (this.element.firstChild) {
      const textarea = this.element.firstChild
      EVENTS.forEach((event) => {
        textarea.removeEventListener(event, this.eventHandler)
      })
    }

    if (this.phantom) {
      document.body.removeChild(this.phantom)
    }
  }

  eventHandler = (event) => {
    const mention = getMentionState(event.target, this.props.value)
    const position = getMentionPosition(
      this.element.firstChild,
      this.phantom,
      this.props.value,
      mention
    )
    this.setState({ mention, position })
  }

  render = () => {
    return (
      <div
        style={{ position: "relative" }}
        ref={(element) => {
          if (element) {
            this.element = element
          }
        }}
      >
        {this.props.children}
        {!!this.state.position && (
          <div
            style={{
              position: "absolute",
              top: this.state.position.top,
              left: this.state.position.left,
              background: "#fff",
              border: "1px solid #ccc",
              padding: "4px",
              boxShadow: "0px 0px 3px #999",
            }}
          >
            ...
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
  const position = caret > SCAN_RANGE ? caret - SCAN_RANGE : 0
  const start = value.substr(position, caret).lastIndexOf("@")

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

function setMentions(props, element) {
  $(element).atwho({
    at: "@",
    displayTpl: '<li><img src="${avatar}" alt="">${username}</li>',
    insertTpl: "@${username}",
    searchKey: "username",
    callbacks: {
      remoteFilter: function (query, callback) {
        $.getJSON(misago.get("MENTION_API"), { q: query }, callback)
      },
    },
  })

  $(element).on("inserted.atwho", (event, _storage, source, controller) => {
    const { query } = controller
    const username = source.target.innerText.trim()
    const prefix = event.target.value.substr(0, query.headPos)
    const suffix = event.target.value.substr(query.endPos)

    event.target.value = prefix + username + suffix
    props.onChange(event)

    const caret = query.headPos + username.length
    event.target.setSelectionRange(caret, caret)
    event.target.focus()
  })
}
