import React from "react"
import classnames from "classnames"

const CLASS_DEFAULT = "posting-open"
const CLASS_MINIMIZED = "posting-minimized"
const CLASS_FULLSCREEN = "posting-fullscreen"

class PostingDialog extends React.Component {
  componentDidMount() {
    document.body.classList.add(CLASS_DEFAULT)
  }

  componentWillUnmount() {
    document.body.classList.remove(CLASS_DEFAULT)
    document.body.classList.remove(CLASS_MINIMIZED)
    document.body.classList.remove(CLASS_FULLSCREEN)
  }

  componentWillReceiveProps({ fullscreen, minimized }) {
    if (minimized) {
      document.body.classList.remove(CLASS_FULLSCREEN)
      document.body.classList.add(CLASS_MINIMIZED)
    } else {
      document.body.classList.remove(CLASS_MINIMIZED)

      if (fullscreen) {
        document.body.classList.add(CLASS_FULLSCREEN)
      } else {
        document.body.classList.remove(CLASS_FULLSCREEN)
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
