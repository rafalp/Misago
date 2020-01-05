import { useQuery } from "@apollo/react-hooks"
import { gql } from "apollo-boost"
import React from "react"
import { BrowserRouter as Router, Route, Switch } from "react-router-dom"
import {
  AuthProvider,
  CategoriesProvider,
  RegisterModalProvider,
  SettingsProvider,
} from "../contexts"
import RootError from "../RootError"
import RootLoader from "../RootLoader"
import { useModalState } from "../hooks"
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
const RegisterModal = React.lazy(() => import("../RegisterModal"))

const App: React.FC = () => {
  const registerModal = useModalState()
  const { loading, data, error } = useQuery<IInitialData>(INITIAL_DATA)
  if (loading) return <RootLoader />
  if (error) return <RootError />

  const { auth, categories, settings } = data || { auth: null, categories: [], settings: null }

  return (
    <AppErrorBoundary>
      <AppLanguageLoader language="en">
        <AuthProvider value={auth}>
          <CategoriesProvider value={categories}>
            <SettingsProvider value={settings}>
              <RegisterModalProvider value={registerModal}>
                <Router>
                  <React.Suspense fallback={<div />}>
                    <Navbar
                      settings={settings}
                      user={auth}
                      openRegister={registerModal.openModal}
                    />
                  </React.Suspense>
                  <Switch>
                    <Route path="/">
                      <div>Hello world!</div>
                    </Route>
                  </Switch>
                  <React.Suspense fallback={<div />}>
                    <RegisterModal
                      closeModal={registerModal.closeModal}
                      isOpen={registerModal.isOpen}
                      settings={settings}
                    />
                  </React.Suspense>
                </Router>
              </RegisterModalProvider>
            </SettingsProvider>
          </CategoriesProvider>
        </AuthProvider>
      </AppLanguageLoader>
    </AppErrorBoundary>
  )
}

export default App
