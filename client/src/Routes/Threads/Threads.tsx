import React from "react"
import { Route, Switch } from "react-router-dom"
import { SettingsContext } from "../../Context"
import { RouteErrorBoundary, RouteLoader, RouteNotFound } from "../../UI"
import * as urls from "../../urls"
import { MobileCategoryNavModal } from "./MobileCategoryNav"
import ThreadsAll from "./ThreadsAll"
import ThreadsCategory from "./ThreadsCategory"
import { ThreadsCategoryModalContextProvider } from "./ThreadsCategoryModalContext"

const Threads: React.FC = () => {
  const settings = React.useContext(SettingsContext)

  return (
    <ThreadsCategoryModalContextProvider>
      <MobileCategoryNavModal />
      <Switch>
        <Route
          path={urls.category({ id: ":id", slug: ":slug" })}
          render={() => (
            <RouteErrorBoundary>
              <ThreadsCategory />
            </RouteErrorBoundary>
          )}
          exact
        />
        <Route
          path={settings?.forumIndexThreads ? urls.index() : urls.threads()}
          render={() => (
            <RouteErrorBoundary>
              <ThreadsAll />
            </RouteErrorBoundary>
          )}
          exact
        />
        <Route
          path={urls.index()}
          render={() => (settings ? <RouteNotFound /> : <RouteLoader />)}
        />
      </Switch>
    </ThreadsCategoryModalContextProvider>
  )
}

export default Threads
