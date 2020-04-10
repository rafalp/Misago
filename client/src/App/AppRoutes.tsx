import React, { Suspense, lazy } from "react"
import { Route, Switch } from "react-router-dom"
import { SettingsContext } from "../Context"
import { CategoriesList, ThreadsList } from "../Routes"
import { RouteErrorBoundary, RouteLoader } from "../UI"
import * as urls from "../urls"

const StartThreadRoute = lazy(() => import("../StartThreadRoute"))
const ThreadRoute = lazy(() => import("../ThreadRoute"))
const UserRoute = lazy(() => import("../UserRoute"))

const sluggable = { id: ":id", slug: ":slug" }

const AppRoutes: React.FC = () => {
  const settings = React.useContext(SettingsContext)

  return (
    <Suspense fallback={<RouteLoader />}>
      <Switch>
        <Route
          path={urls.startThread()}
          render={() => (
            <RouteErrorBoundary>
              <StartThreadRoute />
            </RouteErrorBoundary>
          )}
        />
        <Route
          path={urls.thread(sluggable)}
          render={() => (
            <RouteErrorBoundary>
              <ThreadRoute />
            </RouteErrorBoundary>
          )}
        />
        <Route
          path={urls.user(sluggable)}
          render={() => (
            <RouteErrorBoundary>
              <UserRoute />
            </RouteErrorBoundary>
          )}
        />
        <Route
          path={settings?.forumIndexThreads ? urls.categories() : urls.index()}
          render={() => (
            <RouteErrorBoundary>
              <CategoriesList />
            </RouteErrorBoundary>
          )}
          exact
        />
        <Route path="/" component={ThreadsList} />
      </Switch>
    </Suspense>
  )
}

export default AppRoutes
