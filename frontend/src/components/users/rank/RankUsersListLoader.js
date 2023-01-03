import React from "react"
import UsersList from "misago/components/users-list"

class RankUsersListLoader extends React.Component {
  shouldComponentUpdate() {
    return false
  }

  render = () => <UsersList cols={4} isReady={false} />
}

export default RankUsersListLoader
