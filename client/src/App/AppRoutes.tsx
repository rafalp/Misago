import React, { Suspense, lazy } from "react"
import { Route, Switch } from "react-router-dom"
import { SettingsContext } from "../Context"
import { CategoriesList, ThreadsList } from "../Routes"
import { RouteLoader } from "../UI"
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
        <Route path={urls.startThread()} component={StartThreadRoute} />
        <Route path={urls.thread(sluggable)} component={ThreadRoute} />
        <Route path={urls.user(sluggable)} component={UserRoute} />
        <Route
          path={settings?.forumIndexThreads ? urls.categories() : urls.index()}
          component={CategoriesList}
          exact
        />
        <Route path="/" component={ThreadsList} />
      </Switch>
    </Suspense>
  )
}

export default AppRoutes
