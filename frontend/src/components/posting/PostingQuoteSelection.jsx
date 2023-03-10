import React from "react"
import posting from "../../services/posting"
import { getGlobalState, getQuoteMarkup } from "../posting"

export default class PostingQuoteSelection extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      range: null,
      rect: null,
    }

    this.element = null
  }

  selected = () => {
    if (this.element) {
      const range = getQuoteSelection(this.element) || null
      const rect = range ? range.getBoundingClientRect() : null

      this.setState({ range, rect })
    }
  }

  reply = () => {
    if (!posting.isOpen()) {
      const content = getQuoteMarkup(this.state.range)
      posting.open(Object.assign({}, this.props.posting, { default: content }))

      this.setState({ range: null, rect: null })

      window.setTimeout(focusEditor, 1000)
    } else {
      const globalState = getGlobalState()
      if (globalState && !globalState.disabled) {
        globalState.quote(getQuoteMarkup(this.state.range))
        this.setState({ range: null, rect: null })
        focusEditor()
      }
    }
  }

  render = () => (
    <div>
      <div
        ref={(element) => {
          if (element) {
            this.element = element
          }
        }}
        onMouseUp={this.selected}
        onTouchEnd={this.selected}
      >
        {this.props.children}
      </div>
      {!!this.state.rect && (
        <div
          className="quote-control"
          style={{
            position: "absolute",
            left: this.state.rect.left + window.scrollX,
            top: this.state.rect.bottom + window.scrollY,
          }}
        >
          <div className="quote-control-arrow" />
          <div className="quote-control-inner">
            <button
              className="btn quote-control-btn"
              type="button"
              onClick={this.reply}
            >
              {pgettext("post reply", "Quote")}
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

function focusEditor() {
  const textarea = document.querySelector("#posting-mount textarea")
  textarea.focus()
  textarea.selectionStart = textarea.selectionEnd = textarea.value.length
}

const getQuoteSelection = (container) => {
  if (typeof window.getSelection === "undefined") return

  // Validate that selection is of valid type and has one range
  const selection = window.getSelection()
  if (!selection) return
  if (selection.type !== "Range") return
  if (selection.rangeCount !== 1) return

  // Validate that selection is within the container and post's article
  const range = selection.getRangeAt(0)
  if (!isRangeContained(range, container)) return
  if (!isPostContained(range)) return
  if (!isAnyTextSelected(range.cloneContents())) return

  return range
}

const isRangeContained = (range, container) => {
  const node = range.commonAncestorContainer
  if (node === container) return true

  let p = node.parentNode
  while (p) {
    if (p === container) return true
    p = p.parentNode
  }

  return false
}

const isPostContained = (range) => {
  const element = range.commonAncestorContainer
  if (element.nodeName === "ARTICLE") return true
  if (element.dataset && element.dataset.noquote === "1") return false
  let p = element.parentNode
  while (p) {
    if (p.dataset && p.dataset.noquote === "1") return false
    if (p.nodeName === "ARTICLE") return true
    p = p.parentNode
  }
  return false
}

const isAnyTextSelected = (node) => {
  for (let i = 0; i < node.childNodes.length; i++) {
    const child = node.childNodes[i]
    if (child.nodeType === Node.TEXT_NODE) {
      if (child.textContent && child.textContent.trim().length > 0) return true
    }
    if (child.nodeName === "IMG") return true
    if (isAnyTextSelected(child)) return true
  }

  return false
}
