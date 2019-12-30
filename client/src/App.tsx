import { useQuery } from "@apollo/react-hooks"
import { gql } from "apollo-boost"
import React from "react"
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom"
import Navbar from "./Navbar"
import { AppContainer, RootSpinner } from "./UI"
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

const App: React.FC = () => {
  const { loading, data, error } = useQuery<IInitialData>(INITIAL_DATA)

  return (
    <AppContainer>
      {loading ? (
        <RootSpinner />
      ) : error || !data ? (
        <div>ERROR</div>
      ) : (
        <Router>
          <Navbar settings={data.settings} user={data.auth} />
        </Router>
      )}
    </AppContainer>
  )
}

export default App
