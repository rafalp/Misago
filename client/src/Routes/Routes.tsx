import React, { Suspense, lazy } from "react"
import { Route, Switch } from "react-router-dom"
import { useSettingsContext } from "../Context"
import RouteErrorBoundary from "../UI/RouteErrorBoundary"
import RouteLoader from "../UI/RouteLoader"
import * as urls from "../urls"

const Categories = lazy(() => import("./Categories"))
const PostThread = lazy(() => import("./PostThread"))
const Threads = lazy(() => import("./Threads"))
const Thread = lazy(() => import("./Thread"))
const User = lazy(() => import("./User"))

const sluggable = { id: ":id", slug: ":slug" }

const Routes: React.FC = () => {
  const settings = useSettingsContext()

  return (
    <>
      <Suspense fallback={<RouteLoader />}>
        <Switch>
          <Route
            path={urls.postThread()}
            render={() => (
              <RouteErrorBoundary>
                <PostThread />
              </RouteErrorBoundary>
            )}
            exact
          />
          <Route
            path={urls.postThread(sluggable)}
            render={() => (
              <RouteErrorBoundary>
                <PostThread />
              </RouteErrorBoundary>
            )}
            exact
          />
          <Route
            path={urls.thread(sluggable)}
            render={() => (
              <RouteErrorBoundary>
                <Thread />
              </RouteErrorBoundary>
            )}
          />
          <Route
            path={urls.user(sluggable)}
            render={() => (
              <RouteErrorBoundary>
                <User />
              </RouteErrorBoundary>
            )}
          />
          <Route
            path={
              settings.forumIndexThreads ? urls.categories() : urls.index()
            }
            render={() => (
              <RouteErrorBoundary>
                <Categories />
              </RouteErrorBoundary>
            )}
            exact
          />
          <Route path="/" component={Threads} />
        </Switch>
      </Suspense>
    </>
  )
}

export default Routes
