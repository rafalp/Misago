import React from "react"
import Participants from "misago/components/participants"
import { Poll } from "misago/components/poll"
import PostsList from "misago/components/posts-list"
import Header from "./header"
import * as participants from "misago/reducers/participants"
import * as poll from "misago/reducers/poll"
import * as posts from "misago/reducers/posts"
import * as thread from "misago/reducers/thread"
import ajax from "misago/services/ajax"
import polls from "misago/services/polls"
import snackbar from "misago/services/snackbar"
import posting from "misago/services/posting"
import store from "misago/services/store"
import title from "misago/services/page-title"
import ThreadToolbarBottom from "./ThreadToolbarBottom"
import ThreadToolbarTop from "./ThreadToolbarTop"

export default class extends React.Component {
  componentDidMount() {
    if (this.shouldFetchData()) {
      this.fetchData()
      this.setPageTitle()
    }

    this.startPollingApi()
  }

  componentDidUpdate() {
    if (this.shouldFetchData()) {
      this.fetchData()
      this.startPollingApi()
      this.setPageTitle()
    }
  }

  componentWillUnmount() {
    this.stopPollingApi()
  }

  shouldFetchData() {
    if (this.props.posts.isLoaded) {
      const page = (this.props.params.page || 1) * 1
      return page != this.props.posts.page
    } else {
      return false
    }
  }

  fetchData() {
    store.dispatch(posts.unload())

    ajax
      .get(
        this.props.thread.api.posts.index,
        {
          page: this.props.params.page || 1,
        },
        "posts"
      )
      .then(
        (data) => {
          this.update(data)
        },
        (rejection) => {
          snackbar.apiError(rejection)
        }
      )
  }

  startPollingApi() {
    polls.start({
      poll: "thread-posts",

      url: this.props.thread.api.posts.index,
      data: {
        page: this.props.params.page || 1,
      },
      update: this.update,

      frequency: 120 * 1000,
      delayed: true,
    })
  }

  stopPollingApi() {
    polls.stop("thread-posts")
  }

  setPageTitle() {
    title.set({
      title: this.props.thread.title,
      parent: this.props.thread.category.name,
      page: (this.props.params.page || 1) * 1,
    })
  }

  update = (data) => {
    store.dispatch(thread.replace(data))
    store.dispatch(posts.load(data.post_set))

    if (data.participants) {
      store.dispatch(participants.replace(data.participants))
    }

    if (data.poll) {
      store.dispatch(poll.replace(data.poll))
    }

    this.setPageTitle()
  }

  openPollForm = () => {
    posting.open({
      mode: "POLL",
      submit: this.props.thread.api.poll,

      thread: this.props.thread,
      poll: null,
    })
  }

  openReplyForm = () => {
    posting.open({
      mode: "REPLY",

      config: this.props.thread.api.editor,
      submit: this.props.thread.api.posts.index,
    })
  }

  render() {
    let className = "page page-thread"
    if (this.props.thread.category.css_class) {
      className += " page-thread-" + this.props.thread.category.css_class
    }

    const postsModeration = getPostsModeration(
      this.props.posts.results,
      this.props.user
    )
    const selection = this.props.posts.results.filter((post) => post.isSelected)

    return (
      <div className={className}>
        <div className="page-header-bg">
          <Header {...this.props} />
        </div>
        <div className="container">
          <ThreadToolbarTop
            thread={this.props.thread}
            posts={this.props.posts}
            user={this.props.user}
            selection={selection}
            moderation={postsModeration}
            onPoll={this.openPollForm}
            onReply={this.openReplyForm}
          />
          <Poll
            poll={this.props.poll}
            thread={this.props.thread}
            user={this.props.user}
          />
          <Participants
            participants={this.props.participants}
            thread={this.props.thread}
            user={this.props.user}
          />
          <PostsList {...this.props} />
          <ThreadToolbarBottom
            thread={this.props.thread}
            posts={this.props.posts}
            user={this.props.user}
            selection={selection}
            moderation={postsModeration}
            onReply={this.openReplyForm}
          />
        </div>
      </div>
    )
  }
}

const getPostsModeration = (posts, user) => {
  const moderation = {
    enabled: false,
    approve: false,
    move: false,
    merge: false,
    protect: false,
    hide: false,
    delete: false,
  }

  if (!user.is_authenticated) return moderation

  posts.forEach((post) => {
    if (!post.is_event) {
      if (post.acl.can_approve && post.is_unapproved) {
        moderation.approve = true
      }
      if (post.acl.can_move) moderation.move = true
      if (post.acl.can_merge) moderation.merge = true
      if (post.acl.can_protect || post.acl.can_unprotect) {
        moderation.protect = true
      }
      if (post.acl.can_hide || post.acl.can_unhide) {
        moderation.hide = true
      }
      if (post.acl.can_delete) moderation.delete = true

      if (
        moderation.approve ||
        moderation.move ||
        moderation.merge ||
        moderation.protect ||
        moderation.hide ||
        moderation.delete
      ) {
        moderation.enabled = true
      }
    }
  })

  return moderation
}
