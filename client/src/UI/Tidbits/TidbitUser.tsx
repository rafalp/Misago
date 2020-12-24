import { Link } from "react-router-dom"
import React from "react"
import * as urls from "../../urls"
import TidbitItem from "./TidbitItem"

interface TidbitUserProps {
  user?: {
    id: string
    slug: string
    name: string
  } | null
  name?: string | null
}

const TidbitUser: React.FC<TidbitUserProps> = ({ user, name }) => (
  <TidbitItem className="tidbit-user">
    {user ? <Link to={urls.user(user)}>{user.name}</Link> : name}
  </TidbitItem>
)

export default TidbitUser
