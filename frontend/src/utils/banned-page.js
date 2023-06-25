import moment from "moment"
import React from "react"
import ReactDOM from "react-dom"
import { Provider, connect } from "react-redux"
import BannedPage from "misago/components/banned-page"
import misago from "misago/index"
import store from "misago/services/store"

let select = function (state) {
  return state.tick
}

let RedrawedBannedPage = connect(select)(BannedPage)

export default function (ban, changeState) {
  ReactDOM.render(
    <Provider store={store.getStore()}>
      <RedrawedBannedPage
        message={ban.message}
        expires={ban.expires_on ? moment(ban.expires_on) : null}
      />
    </Provider>,

    document.getElementById("page-mount")
  )

  if (typeof changeState === "undefined" || changeState) {
    let forumName = misago.get("SETTINGS").forum_name
    document.title =
      pgettext("banned error title", "You are banned") + " | " + forumName
    window.history.pushState({}, "", misago.get("BANNED_URL"))
  }
}
