import React from "react"
import ThreadPreview from "misago/components/threads-list/thread/preview"

export default class extends React.Component {
  shouldComponentUpdate() {
    return false
  }

  render() {
    return (
      <div className="threads-list ui-preview">
        <ul className="list-group">
          <ThreadPreview />
        </ul>
      </div>
    )
  }
}
