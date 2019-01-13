import React from "react"
import ItemPreview from "misago/components/users/active-posters/list-item-preview"
import * as random from "misago/utils/random"

export default class extends React.Component {
  shouldComponentUpdate() {
    return false
  }

  render() {
    return (
      <div className="active-posters-list">
        <div className="container">
          <p className="lead ui-preview">
            <span
              className="ui-preview-text"
              style={{ width: random.int(50, 220) + "px" }}
            >
              &nbsp;
            </span>
          </p>

          <div className="active-posters ui-preview">
            <ul className="list-group">
              {[0, 1, 2].map(i => {
                return <ItemPreview hiddenOnMobile={i > 0} key={i} />
              })}
            </ul>
          </div>
        </div>
      </div>
    )
  }
}
