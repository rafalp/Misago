import { useApolloClient } from "@apollo/react-hooks"
import React from "react"
import { AUTH_USER } from "../auth"
import { useStorageEvent } from "../localStorage"
import AuthChangedLoggedInAlert from "./AuthChangedLoggedInAlert"
import AuthChangedLoggedOutAlert from "./AuthChangedLoggedOutAlert"

interface User {
  id: string
  name: string
}

interface UserUpdate {
  newValue: User | null
  oldValue: User | null
}

interface AuthChangedAlertProps {
  user: User | null
}

const AuthChangedAlert: React.FC<AuthChangedAlertProps> = ({ user }) => {
  const client = useApolloClient()

  const [initialUser, setInitialUser] = React.useState(user)

  const userUpdateJson = useStorageEvent(AUTH_USER)
  const [userUpdate, setUserUpdate] = React.useState<UserUpdate | undefined>(
    undefined
  )

  React.useEffect(() => {
    if (userUpdateJson) {
      setUserUpdate({
        newValue: parseUserJSON(userUpdateJson.newValue),
        oldValue: parseUserJSON(userUpdateJson.oldValue),
      })
    }
  }, [userUpdateJson])

  React.useEffect(() => {
    setUserUpdate({
      newValue: user,
      oldValue: initialUser,
    })
    setInitialUser(user)
  }, [initialUser, user])

  if (!userUpdate) return null

  const newId = userUpdate.newValue?.id
  const oldId = userUpdate.oldValue?.id

  if (newId && newId !== oldId) {
    return (
      <AuthChangedLoggedInAlert
        username={userUpdate.newValue?.name || ""}
        reload={client.resetStore}
      />
    )
  }
  if (oldId && !newId) {
    return (
      <AuthChangedLoggedOutAlert
        username={userUpdate.oldValue?.name || ""}
        reload={client.resetStore}
      />
    )
  }

  return null
}

const parseUserJSON = (data: string | null): User | null => {
  if (!data) return null
  try {
    const parsedData = JSON.parse(data)
    return {
      id: String(parsedData.id),
      name: String(parsedData.name),
    }
  } catch (_) {
    return null
  }
}

export default AuthChangedAlert
