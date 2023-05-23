import React from "react"
import Participants from "misago/components/participants"
import { Poll, PollForm } from "misago/components/poll"
import PostsList from "misago/components/posts-list"
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
import { PostingQuoteSelection } from "../posting"
import PageContainer from "../PageContainer"
import ThreadHeader from "./ThreadHeader"
import ThreadToolbarBottom from "./ThreadToolbarBottom"
import ThreadToolbarThird from "./ThreadToolbarThird"
import ThreadToolbarTop from "./ThreadToolbarTop"

export default class extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      editPoll: false,
    }
  }

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
    this.setState({ editPoll: true })
  }

  closePollForm = () => {
    this.setState({ editPoll: false })
  }

  openReplyForm = () => {
    posting.open({
      mode: "REPLY",

      thread: this.props.thread,
      config: this.props.thread.api.editor,
      submit: this.props.thread.api.posts.index,
    })
  }

  render() {
    const category = this.props.thread.category

    let className = "page page-thread"
    if (category.css_class) {
      className += " page-thread-" + category.css_class
    }

    const styleName =
      category.special_role === "private_threads"
        ? "private-threads"
        : category.css_class || "category-threads"

    const threadModeration = getThreadModeration(
      this.props.thread,
      this.props.user
    )

    const postsModeration = getPostsModeration(
      this.props.posts.results,
      this.props.user
    )
    const selection = this.props.posts.results.filter((post) => post.isSelected)

    return (
      <div className={className}>
        <ThreadHeader
          styleName={styleName}
          thread={this.props.thread}
          posts={this.props.posts}
          user={this.props.user}
          moderation={threadModeration}
        />
        <PageContainer>
          <Participants
            participants={this.props.participants}
            thread={this.props.thread}
            user={this.props.user}
          />
          <ThreadToolbarTop
            thread={this.props.thread}
            posts={this.props.posts}
            user={this.props.user}
            selection={selection}
            moderation={postsModeration}
            pollDisabled={this.state.editPoll}
            onPoll={this.openPollForm}
            onReply={this.openReplyForm}
          />
          {this.state.editPoll ? (
            <PollForm
              poll={this.props.poll}
              thread={this.props.thread}
              close={this.closePollForm}
            />
          ) : (
            <Poll
              poll={this.props.poll}
              thread={this.props.thread}
              user={this.props.user}
              edit={this.openPollForm}
            />
          )}
          {this.props.thread.acl.can_reply ? (
            <PostingQuoteSelection
              posting={{
                mode: "REPLY",

                thread: this.props.thread,
                config: this.props.thread.api.editor,
                submit: this.props.thread.api.posts.index,
              }}
            >
              <PostsList {...this.props} />
            </PostingQuoteSelection>
          ) : (
            <PostsList {...this.props} />
          )}
          <ThreadToolbarBottom
            thread={this.props.thread}
            posts={this.props.posts}
            user={this.props.user}
            selection={selection}
            moderation={postsModeration}
            onReply={this.openReplyForm}
          />
          <ThreadToolbarThird />
        </PageContainer>
      </div>
    )
  }
}

const getThreadModeration = (thread, user) => {
  const moderation = {
    enabled: false,
    edit: false,
    approve: false,
    close: false,
    open: false,
    hide: false,
    unhide: false,
    move: false,
    merge: false,
    pinGlobally: false,
    pinLocally: false,
    unpin: false,
    delete: false,
  }

  if (!user.is_authenticated) return moderation

  moderation.edit = thread.acl.can_edit
  moderation.approve = thread.acl.can_approve && thread.is_unapproved
  moderation.close = thread.acl.can_close && !thread.is_closed
  moderation.open = thread.acl.can_close && thread.is_closed
  moderation.hide = thread.acl.can_hide && !thread.is_hidden
  moderation.unhide = thread.acl.can_unhide && thread.is_hidden
  moderation.move = thread.acl.can_move
  moderation.merge = thread.acl.can_merge
  moderation.pinGlobally = thread.acl.can_pin_globally && thread.weight < 2
  moderation.pinLocally = thread.acl.can_pin && thread.weight !== 1
  moderation.unpin =
    (thread.acl.can_pin && thread.weight === 1) ||
    (thread.acl.can_pin_globally && thread.weight === 2)
  moderation.delete = thread.acl.can_delete

  moderation.enabled =
    moderation.edit ||
    moderation.approve ||
    moderation.close ||
    moderation.open ||
    moderation.hide ||
    moderation.unhide ||
    moderation.move ||
    moderation.merge ||
    moderation.pinGlobally ||
    moderation.pinLocally ||
    moderation.unpin ||
    moderation.delete

  return moderation
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
