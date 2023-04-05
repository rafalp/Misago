import React from "react"
import ajax from "misago/services/ajax"

export default class extends React.Component {
  constructor(props) {
    super(props)

    this.initialized = false
    this.primed = false
    this.observer = null
  }

  initialize = (element) => {
    this.initialized = true

    this.observer = new IntersectionObserver((entries) =>
      entries.forEach(this.callback)
    )
    this.observer.observe(element)
  }

  callback = (entry) => {
    if (!entry.isIntersecting || this.props.post.is_read || this.primed) {
      return
    }

    window.setTimeout(() => {
      ajax.post(this.props.post.api.read)
    }, 0)

    this.primed = true
    this.destroy()
  }

  destroy() {
    if (this.observer) {
      this.observer.disconnect()
      this.observer = null
    }
  }

  componentWillUnmount() {
    this.destroy()
  }

  render() {
    const ready = !this.initialized && !this.primed && !this.props.post.is_read

    return (
      <div
        className={this.props.className}
        ref={(node) => {
          if (node && ready) {
            this.initialize(node)
          }
        }}
      >
        {this.props.children}
      </div>
    )
  }
}
