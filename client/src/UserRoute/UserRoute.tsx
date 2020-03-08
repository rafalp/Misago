import React from "react"
import { useParams } from "react-router-dom"
import { WindowTitle } from "../UI"
import UserQuery from "./UserQuery"

interface IUserRouteParams {
  id: string
}

const UserRoute: React.FC = () => {
  const { id } = useParams<IUserRouteParams>()

  return (
    <UserQuery id={id}>
      {({ data: { user } }) => (
        <>
          <WindowTitle title={user.name} />
          <h1>{user.name}</h1>
        </>
      )}
    </UserQuery>
  )
}

export default UserRoute
