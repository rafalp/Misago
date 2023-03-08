import React from "react"
import classnames from "classnames"

const CLASS_ACTIVE = "posting-active"
const CLASS_DEFAULT = "posting-default"
const CLASS_MINIMIZED = "posting-minimized"
const CLASS_FULLSCREEN = "posting-fullscreen"

class PostingDialog extends React.Component {
  componentDidMount() {
    document.body.classList.add(CLASS_ACTIVE, CLASS_DEFAULT)
  }

  componentWillUnmount() {
    document.body.classList.remove(
      CLASS_ACTIVE,
      CLASS_DEFAULT,
      CLASS_MINIMIZED,
      CLASS_FULLSCREEN
    )
  }

  componentWillReceiveProps({ fullscreen, minimized }) {
    if (minimized) {
      document.body.classList.remove(CLASS_DEFAULT, CLASS_FULLSCREEN)
      document.body.classList.add(CLASS_MINIMIZED)
    } else {
      if (fullscreen) {
        document.body.classList.remove(CLASS_DEFAULT, CLASS_MINIMIZED)
        document.body.classList.add(CLASS_FULLSCREEN)
      } else {
        document.body.classList.remove(CLASS_FULLSCREEN, CLASS_MINIMIZED)
        document.body.classList.add(CLASS_DEFAULT)
      }
    }
  }

  render() {
    const { children, fullscreen, minimized } = this.props

    return (
      <div
        className={classnames("posting-dialog", {
          "posting-dialog-minimized": minimized,
          "posting-dialog-fullscreen": fullscreen && !minimized,
        })}
      >
        <div className="posting-dialog-container">{children}</div>
      </div>
    )
  }
}

export default PostingDialog
