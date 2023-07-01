import React from "react"
import PostFeed from "misago/components/post-feed"
import Button from "misago/components/button"
import MisagoMarkup from "misago/components/misago-markup"
import {
  update as updatePosts,
  append as appendPosts,
} from "misago/reducers/posts"
import { updateProvider } from "misago/reducers/search"
import ajax from "misago/services/ajax"
import snackbar from "misago/services/snackbar"
import store from "misago/services/store"

export default function (props) {
  return (
    <div>
      <PostFeed isReady={true} posts={props.results} />
      <LoadMore {...props} />
    </div>
  )
}

export class LoadMore extends React.Component {
  onClick = () => {
    store.dispatch(
      updatePosts({
        isBusy: true,
      })
    )

    ajax
      .get(this.props.provider.api, {
        q: this.props.query,
        page: this.props.next,
      })
      .then(
        (providers) => {
          providers.forEach((provider) => {
            if (provider.id !== "threads") return
            store.dispatch(appendPosts(provider.results))
            store.dispatch(updateProvider(provider))
          })

          store.dispatch(
            updatePosts({
              isBusy: false,
            })
          )
        },
        (rejection) => {
          snackbar.apiError(rejection)

          store.dispatch(
            updatePosts({
              isBusy: false,
            })
          )
        }
      )
  }

  render() {
    if (!this.props.more) return null

    return (
      <div className="pager-more">
        <Button
          className="btn btn-default btn-outline"
          loading={this.props.isBusy}
          onClick={this.onClick}
        >
          {pgettext("search threads btn", "Show more")}
        </Button>
      </div>
    )
  }
}
