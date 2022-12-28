import React from "react"
import stringCount from "misago/utils/string-count"

export default class extends React.Component {
  getClassName() {
    if (this.props.copy && this.props.copy.length) {
      if (
        stringCount(this.props.copy, "<p") === 1 &&
        this.props.copy.indexOf("<br") === -1
      ) {
        return "page-lead lead"
      }
    }

    return "page-lead"
  }

  render() {
    if (this.props.copy && this.props.copy.length) {
      return (
        <div
          className={this.getClassName()}
          dangerouslySetInnerHTML={{
            __html: this.props.copy,
          }}
        />
      )
    } else {
      return null
    }
  }
}
