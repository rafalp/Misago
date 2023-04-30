import classnames from "classnames"
import React from "react"
import { connect } from "react-redux"
import { close } from "../../reducers/overlay"

const BODY_CLASS = "has-overlay"

class Overlay extends React.Component {
  constructor(props) {
    super(props)

    this.scrollOrigin = null
  }

  componentDidUpdate(prevProps) {
    if (prevProps.open !== this.props.open) {
      if (this.props.open) {
        this.scrollOrigin = window.pageYOffset
        document.body.classList.add(BODY_CLASS)
        if (this.props.onOpen) {
          this.props.onOpen()
        }
      } else {
        document.body.classList.remove(BODY_CLASS)
        window.scrollTo(0, this.scrollOrigin)
        this.scrollOrigin = null
      }
    }
  }

  closeOnNavigation = (event) => {
    if (event.target.closest("a")) {
      this.props.dispatch(close())
    }
  }

  render() {
    return (
      <div
        className={classnames("overlay", this.props.className, {
          "overlay-open": this.props.open,
        })}
        onClick={this.closeOnNavigation}
      >
        {this.props.children}
      </div>
    )
  }
}

const OverlayConnected = connect()(Overlay)

export default OverlayConnected
