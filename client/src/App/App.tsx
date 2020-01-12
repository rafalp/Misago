import { useQuery } from "@apollo/react-hooks"
import { gql } from "apollo-boost"
import React from "react"
import { BrowserRouter as Router, Route, Switch } from "react-router-dom"
import { AuthModalProvider, AuthContext, CategoriesContext, SettingsContext } from "../Context"
import { ICategory, ISettings, IUser } from "../types"
import AppError from "./AppError"
import AppLoader from "./AppLoader"
import AppErrorBoundary from "./AppErrorBoundary"
import AppLanguageLoader from "./AppLanguageLoader"

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
      passwordMinLength
      passwordMaxLength
      usernameMinLength
      usernameMaxLength
    }
  }
`

interface IInitialData {
  auth: IUser
  categories: Array<ICategory>
  settings: ISettings
}

const Navbar = React.lazy(() => import("../Navbar"))
const AuthModal = React.lazy(() => import("../AuthModal"))

const App: React.FC = () => {
  const { loading, data, error } = useQuery<IInitialData>(INITIAL_DATA)
  if (loading) return <AppLoader />
  if (error) return <AppError />

  const { auth, categories, settings } = data || { auth: null, categories: [], settings: null }

  return (
    <AppErrorBoundary>
      <AppLanguageLoader language="en">
        <AuthContext.Provider value={auth}>
          <CategoriesContext.Provider value={categories}>
            <SettingsContext.Provider value={settings}>
              <AuthModalProvider>
                <Router>
                  <React.Suspense fallback={<div />}>
                    <Navbar settings={settings} user={auth} />
                  </React.Suspense>
                  <Switch>
                    <Route path="/">
                      <div>Hello world!</div>
                    </Route>
                  </Switch>
                  <React.Suspense fallback={<div />}>
                    <AuthModal settings={settings} />
                  </React.Suspense>
                </Router>
              </AuthModalProvider>
            </SettingsContext.Provider>
          </CategoriesContext.Provider>
        </AuthContext.Provider>
      </AppLanguageLoader>
    </AppErrorBoundary>
  )
}

export default App
