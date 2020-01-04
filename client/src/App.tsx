import { useQuery } from "@apollo/react-hooks"
import { gql } from "apollo-boost"
import React from "react"
import { BrowserRouter as Router, Switch } from "react-router-dom"
import RootLoader from "./RootLoader"
import { ICategory, ISettings, IUser } from "./types"

interface IInitialData {
  auth: IUser
  categories: Array<ICategory>
  settings: ISettings
}

const INITIAL_DATA = gql`
  query InitialData {
    auth {
      id
      name
      avatars {
        size
        url
      }
    }
    categories {
      id
      name
      slug
      color
      children {
        id
        name
        slug
        color
      }
    }
    settings {
      forumName
    }
  }
`

const Navbar = React.lazy(() => import("./Navbar"))

const App: React.FC = () => {
  const { loading, data, error } = useQuery<IInitialData>(INITIAL_DATA)
  if (loading) return <RootLoader />
  if (error) return <div>ERROR</div>

  return (
    <Router>
      <Navbar settings={data && data.settings} user={data && data.auth} />
      <Switch>
        <div>ROUTE</div>
      </Switch>
    </Router>
  )
}

export default App
