import { useQuery } from "@apollo/react-hooks"
import { gql } from "apollo-boost"
import React from "react"
import { BrowserRouter as Router, Route, Switch } from "react-router-dom"
import RootError from "../RootError"
import RootLoader from "../RootLoader"
import { ICategory, ISettings, IUser } from "../types"
import AppErrorBoundary from "./AppErrorBoundary"
import AppLanguageLoader from "./AppLanguageLoader"

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

const Navbar = React.lazy(() => import("../Navbar"))

const App: React.FC = () => {
  const { loading, data, error } = useQuery<IInitialData>(INITIAL_DATA)
  if (loading) return <RootLoader />
  if (error) return <RootError />

  return (
    <AppErrorBoundary>
      <AppLanguageLoader language="en">
        <Router>
          <React.Suspense fallback={<div />}>
            <Navbar settings={data && data.settings} user={data && data.auth} />
          </React.Suspense>
          <Switch>
            <Route path="/">
              <div>Hello world!</div>
            </Route>
          </Switch>
        </Router>
      </AppLanguageLoader>
    </AppErrorBoundary>
  )
}

export default App
