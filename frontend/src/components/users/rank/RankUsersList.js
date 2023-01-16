import React from "react"
import UsersList from "../../users-list"

const RankUsersList = ({ users }) => (
  <UsersList cols={4} isReady={true} showStatus={true} users={users} />
)

export default RankUsersList
