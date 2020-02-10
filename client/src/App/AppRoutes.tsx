import React, { Suspense, lazy } from "react"
import { Route, Switch } from "react-router-dom"
import { PageLoader } from "../UI"

const ThreadsPage = lazy(() => import("../ThreadsPage"))

const AppRoutes: React.FC = () => (
  <Suspense fallback={<PageLoader />}>
    <Switch>
      <Route path="/" component={ThreadsPage} />
    </Switch>
  </Suspense>
)

export default AppRoutes
