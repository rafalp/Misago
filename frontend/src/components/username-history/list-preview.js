import React from "react"
import ChangePreview from "misago/components/username-history/change-preview"

export default class extends React.Component {
  shouldComponentUpdate() {
    return false
  }

  render() {
    return (
      <div className="username-history ui-preview">
        <ul className="list-group">
          {[0, 1, 2].map((i) => {
            return <ChangePreview hiddenOnMobile={i > 0} key={i} />
          })}
        </ul>
      </div>
    )
  }
}
