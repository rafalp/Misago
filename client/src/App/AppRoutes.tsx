import React, { Suspense, lazy } from "react"
import { Route, Switch } from "react-router-dom"
import { RouteLoader } from "../UI"

const ThreadsRoute = lazy(() => import("../ThreadsRoute"))

const AppRoutes: React.FC = () => (
  <Suspense fallback={<RouteLoader />}>
    <Switch>
      <Route path="/" component={ThreadsRoute} />
    </Switch>
  </Suspense>
)

export default AppRoutes
