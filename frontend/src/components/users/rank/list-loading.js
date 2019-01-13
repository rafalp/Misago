import React from "react"
import UsersList from "misago/components/users-list"

export default class extends React.Component {
  shouldComponentUpdate() {
    return false
  }

  render() {
    return (
      <div>
        <UsersList cols={4} isReady={false} />
      </div>
    )
  }
}
