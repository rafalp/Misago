import React from "react"
import Change from "misago/components/username-history/change"

export default class extends React.Component {
  render() {
    return (
      <div className="username-history ui-ready">
        <ul className="list-group">
          {this.props.changes.map((change) => {
            return <Change change={change} key={change.id} />
          })}
        </ul>
      </div>
    )
  }
}
