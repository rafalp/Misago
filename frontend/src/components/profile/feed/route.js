import React from "react"
import PostFeed from "misago/components/post-feed"
import Button from "misago/components/button"
import * as posts from "misago/reducers/posts"
import title from "misago/services/page-title"
import ajax from "misago/services/ajax"
import snackbar from "misago/services/snackbar"
import store from "misago/services/store"

export default class extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      isLoading: false
    }
  }

  loadItems(start = 0) {
    ajax
      .get(this.props.api, {
        start: start || 0
      })
      .then(
        data => {
          if (start === 0) {
            store.dispatch(posts.load(data))
          } else {
            store.dispatch(posts.append(data))
          }

          this.setState({
            isLoading: false
          })
        },
        rejection => {
          this.setState({
            isLoading: false
          })

          snackbar.apiError(rejection)
        }
      )
  }

  loadMore = () => {
    this.setState({
      isLoading: true
    })

    this.loadItems(this.props.posts.next)
  }

  componentDidMount() {
    title.set({
      title: this.props.title,
      parent: this.props.profile.username
    })

    this.loadItems()
  }

  render() {
    return (
      <div className="profile-feed">
        <nav className="toolbar">
          <h3 className="toolbar-left">{this.props.header}</h3>
        </nav>
        <Feed
          isLoading={this.state.isLoading}
          loadMore={this.loadMore}
          {...this.props}
        />
      </div>
    )
  }
}

export function Feed(props) {
  if (!props.posts.results.length) {
    return <p className="lead">{props.emptyMessage}</p>
  }

  return (
    <div>
      <PostFeed
        isReady={props.posts.isLoaded}
        posts={props.posts.results}
        poster={props.profile}
      />
      <LoadMoreButton
        isLoading={props.isLoading}
        loadMore={props.loadMore}
        next={props.posts.next}
      />
    </div>
  )
}

export function LoadMoreButton(props) {
  if (!props.next) return null

  return (
    <div className="pager-more">
      <Button
        className="btn btn-default btn-outline"
        loading={props.isLoading}
        onClick={props.loadMore}
      >
        {gettext("Show older activity")}
      </Button>
    </div>
  )
}
