import React from "react"
import { Route } from "react-router-dom"
import * as urls from "../../urls"
import AllThreadsList from "./AllThreadsList"
import CategoryThreadsList from "./CategoryThreadsList"

const ThreadsList: React.FC = () => {
  return (
    <>
      <Route
        path={urls.category({id: ":id", slug: ":slug"})}
        component={CategoryThreadsList}
        exact
      />
      <Route
        path="/"
        component={AllThreadsList}
        exact
      />
    </>
  )
}

export default ThreadsList
