import React from "react"
import DiffMessage from "misago/components/threads-list/list/diff-message"

export default class extends React.Component {
  getDiffMessage() {
    if (this.props.diffSize === 0) return null

    return (
      <DiffMessage
        applyDiff={this.props.applyDiff}
        diffSize={this.props.diffSize}
      />
    )
  }

  render() {
    return (
      <div className="threads-list ui-ready">
        <ul className="list-group">
          {this.getDiffMessage()}
          {this.props.children}
        </ul>
      </div>
    )
  }
}
