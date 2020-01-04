import { useQuery } from "@apollo/react-hooks"
import { Catalogs } from '@lingui/core';
import { I18nProvider } from "@lingui/react"
import { gql } from "apollo-boost"
import React from "react"
import { BrowserRouter as Router, Route, Switch } from "react-router-dom"
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

interface ILanguageLoaderProps {
  children: React.ReactNode
  language: string
}

const LanguageLoader: React.FC<ILanguageLoaderProps> = ({ children, language }) => {
  const [catalogs, setCatalogs] = React.useState<Catalogs>({})

  React.useEffect(() => {
    import(
      /* webpackMode: "lazy", webpackChunkName: "i18n-[index]" */
      `./locale/${language}/messages`
    ).then(catalog => {
      setCatalogs(c => { return {...c, [language]: catalog.default}})
    })
  }, [language])

  if (!catalogs[language]) return <RootLoader />
  return <I18nProvider language={language} catalogs={catalogs}>{children}</I18nProvider>
}

const App: React.FC = () => {
  const { loading, data, error } = useQuery<IInitialData>(INITIAL_DATA)
  if (loading) return <RootLoader />
  if (error) return <div>ERROR</div>

  return (
    <LanguageLoader language="en">
      <Router>
        <React.Suspense fallback={<div/>}>
          <Navbar settings={data && data.settings} user={data && data.auth} />
        </React.Suspense>
        <Switch>
          <Route path="/">
            <div>Hello world!</div>
          </Route>
        </Switch>
      </Router>
    </LanguageLoader>
  )
}

export default App
