import React, { Suspense, lazy } from "react"
import { Route, Switch } from "react-router-dom"
import { CategoriesList, ThreadsList } from "../Routes"
import { RouteLoader } from "../UI"
import * as urls from "../urls"

const StartThreadRoute = lazy(() => import("../StartThreadRoute"))
const ThreadRoute = lazy(() => import("../ThreadRoute"))
const UserRoute = lazy(() => import("../UserRoute"))

const sluggable = { id: ":id", slug: ":slug" }

const AppRoutes: React.FC = () => (
  <Suspense fallback={<RouteLoader />}>
    <Switch>
      <Route path={urls.categories()} component={CategoriesList} />
      <Route path={urls.startThread()} component={StartThreadRoute} />
      <Route path={urls.thread(sluggable)} component={ThreadRoute} />
      <Route path={urls.user(sluggable)} component={UserRoute} />
      <Route path="/" component={ThreadsList} />
    </Switch>
  </Suspense>
)

export default AppRoutes
