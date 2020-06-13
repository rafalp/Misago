import React from "react"
import { Redirect, Route, Switch } from "react-router-dom"
import * as urls from "../../urls"
import ThreadRoute from "./ThreadRoute"

const Thread: React.FC = () => (
  <Switch>
    <Route
      path={urls.thread({ id: ":id", slug: ":slug" })}
      component={ThreadRoute}
      exact
    />
    <Route
      path={urls.threadLastReply({ id: ":id", slug: ":slug" })}
      render={() => <div>Thread last reply</div>}
      exact
    />
    <Route
      path={urls.thread({ id: ":id", slug: ":slug" }) + "1/"}
      render={({ match }) => (
        <Redirect
          to={urls.thread({ id: match.params.id, slug: match.params.slug })}
        />
      )}
      exact
    />
    <Route
      path={urls.thread({ id: ":id", slug: ":slug" }) + ":page/"}
      component={ThreadRoute}
      exact
    />
  </Switch>
)

export default Thread
