import React from "react"
import Button from "misago/components/button"
import {
  compareGlobalWeight,
  compareWeight,
} from "misago/components/threads/compare"
import Container from "misago/components/threads/container"
import {
  diffThreads,
  getModerationActions,
  getPageTitle,
  getTitle,
} from "misago/components/threads/utils"
import ThreadsList from "misago/components/ThreadsList"
import WithDropdown from "misago/components/with-dropdown"
import misago from "misago/index"
import * as select from "misago/reducers/selection"
import { append, deleteThread, hydrate, patch } from "misago/reducers/threads"
import ajax from "misago/services/ajax"
import snackbar from "misago/services/snackbar"
import store from "misago/services/store"
import title from "misago/services/page-title"
import polls from "../../services/polls"
import * as sets from "../../utils/sets"
import {
  PageHeaderHTMLMessage,
  PageHeaderMessage,
  PageHeaderPlain,
} from "../PageHeader"

export default class extends WithDropdown {
  constructor(props) {
    super(props)

    this.state = {
      isLoaded: false,
      isBusy: false,

      diff: {
        results: [],
      },

      moderation: [],
      busyThreads: [],

      dropdown: false,
      subcategories: [],

      next: 0,
    }

    const categoryId = this.getCategoryId()
    if (misago.has("THREADS")) {
      this.initWithPreloadedData(categoryId, misago.get("THREADS"))
    } else {
      this.loadThreads(categoryId, this.props.list.type)
    }
  }

  componentDidMount() {
    this.setPageTitle()

    if (misago.has("THREADS")) {
      // unlike in other components, routes are root components for threads
      // so we can't dispatch store action from constructor
      store.dispatch(hydrate(misago.pop("THREADS").results))

      this.setState({ isLoaded: true })
    }

    store.dispatch(select.none())
  }

  componentDidUpdate(prevProps) {
    const categoryUpdated = this.props.category.id !== prevProps.category.id
    const listUpdated = this.props.list.path !== prevProps.list.path
    
    if (categoryUpdated || listUpdated) {
      polls.stop("threads")
      this.setPageTitle()
      this.loadThreads(this.getCategoryId(), this.getListType())
    }
  }

  getCategoryId() {
    if (!this.props.category.special_role) {
      return this.props.category.id
    } else {
      return null
    }
  }

  getListType() {
    return this.props.list.type
  }

  initWithPreloadedData(categoryId, data) {
    this.state = Object.assign(this.state, {
      moderation: getModerationActions(data.results),
      subcategories: data.subcategories,
      next: data.next,
    })

    this.startPolling(categoryId, this.props.list.type)
  }

  loadThreads(categoryId, listType, next = 0) {
    if (next === 0) {
      this.setState({ isLoaded: false, isBusy: true })
    }

    ajax
      .get(
        this.props.options.api,
        {
          category: categoryId,
          list: listType,
          start: next || 0,
        },
        "threads"
      )
      .then(
        (data) => {
          if (categoryId !== this.getCategoryId() || listType !== this.getListType()) {
            // user changed route before loading completion
            return
          }

          if (next === 0) {
            store.dispatch(hydrate(data.results))
          } else {
            store.dispatch(append(data.results, this.getSorting()))
          }

          this.setState({
            isLoaded: true,
            isBusy: false,

            moderation: getModerationActions(store.getState().threads),

            subcategories: data.subcategories,

            next: data.next,
          })

          this.startPolling(categoryId, listType)
        },
        (rejection) => {
          snackbar.apiError(rejection)
        }
      )
  }

  startPolling(categoryId, listType) {
    polls.start({
      poll: "threads",
      url: this.props.options.api,
      data: {
        category: categoryId,
        list: listType,
      },
      frequency: 120 * 1000,
      update: this.pollResponse,
    })
  }

  getTitle() {
    if (this.props.options.title) {
      return this.props.options.title
    }

    return getTitle(this.props.category)
  }

  setPageTitle() {
    if (this.props.category.level || !misago.get("THREADS_ON_INDEX")) {
      title.set(getPageTitle(this.props.category, this.props.list))
    } else if (this.props.options.title) {
      title.set(this.props.options.title)
    } else {
      const settings = misago.get("SETTINGS")
      const title = settings.index_title || settings.forum_name

      if (this.props.list.path) {
        document.title = this.props.list.longName + " | " + title
      } else {
        document.title = title
      }
    }
  }

  getSorting() {
    if (this.props.category.level) {
      return compareWeight
    } else {
      return compareGlobalWeight
    }
  }

  // AJAX

  loadMore = () => {
    this.setState({
      isBusy: true,
    })

    this.loadThreads(this.getCategoryId(), this.props.list.type, this.state.next)
  }

  pollResponse = (data) => {
    this.setState({
      diff: Object.assign({}, data, {
        results: diffThreads(this.props.threads, data.results),
      }),
    })
  }

  addThreads = (threads) => {
    store.dispatch(append(threads, this.getSorting()))
  }

  applyDiff = () => {
    this.addThreads(this.state.diff.results)

    this.setState(
      Object.assign({}, this.state.diff, {
        moderation: getModerationActions(store.getState().threads),

        diff: {
          results: [],
        },
      })
    )
  }

  // Thread state utils

  freezeThread = (thread) => {
    this.setState(function (currentState) {
      return {
        busyThreads: sets.toggle(currentState.busyThreads, thread),
      }
    })
  }

  updateThread = (thread) => {
    store.dispatch(patch(thread, thread, this.getSorting()))
  }

  deleteThread = (thread) => {
    store.dispatch(deleteThread(thread))
  }

  getMoreButton() {
    if (!this.state.next) return null

    return (
      <div className="pager-more">
        <Button
          className="btn btn-default btn-outline"
          loading={this.state.isBusy || this.state.busyThreads.length}
          onClick={this.loadMore}
        >
          {gettext("Show more")}
        </Button>
      </div>
    )
  }

  getClassName() {
    let className = "page page-threads"
    className += " page-threads-" + this.props.list.type
    if (isIndex(this.props)) {
      className += " page-threads-index"
    }
    if (this.props.category.css_class) {
      className += " page-threads-" + this.props.category.css_class
    }
    return className
  }

  render() {
    const root = this.props.categories[0]
    const { category, list } = this.props
    const specialRole = category.special_role

    return (
      <div className={this.getClassName()}>
        {specialRole == "root_category" &&
          misago.get("THREADS_ON_INDEX") &&
          misago.get("SETTINGS").index_header && (
            <PageHeaderPlain
              header={misago.get("SETTINGS").index_header}
              message={
                category.description && (
                  <PageHeaderHTMLMessage message={category.description.html} />
                )
              }
              styleName="forum-index"
            />
          )}
        {specialRole == "root_category" && !misago.get("THREADS_ON_INDEX") && (
          <PageHeaderPlain header={gettext("Threads")} styleName="threads" />
        )}
        {specialRole == "private_threads" && (
          <PageHeaderPlain
            header={this.props.options.title}
            message={
              this.props.options.pageLead && (
                <PageHeaderMessage>
                  <p>{this.props.options.pageLead}</p>
                </PageHeaderMessage>
              )
            }
            styleName="private-threads"
          />
        )}
        {!specialRole && (
          <PageHeaderPlain
            header={category.name}
            message={
              category.description && (
                <PageHeaderHTMLMessage message={category.description.html} />
              )
            }
            styleName={category.css_class || "category-threads"}
          />
        )}
        <Container
          api={this.props.options.api}
          root={root}
          category={this.props.category}
          categories={this.props.categories}
          categoriesMap={this.props.categoriesMap}
          list={this.props.list}
          lists={this.props.lists}
          user={this.props.user}
          pageLead={this.props.options.pageLead}
          threads={this.props.threads}
          threadsCount={this.state.count}
          moderation={this.state.moderation}
          selection={this.props.selection}
          busyThreads={this.state.busyThreads}
          addThreads={this.addThreads}
          startThread={this.props.options.startThread}
          freezeThread={this.freezeThread}
          deleteThread={this.deleteThread}
          updateThread={this.updateThread}
          isLoaded={this.state.isLoaded}
          isBusy={this.state.isBusy}
        >
          <ThreadsList
            category={category}
            categories={this.props.categoriesMap}
            list={list}
            selection={this.props.selection}
            threads={this.props.threads}
            updatedThreads={this.state.diff.results.length}
            applyUpdate={this.applyDiff}
            showOptions={!!this.props.user.id}
            isLoaded={this.state.isLoaded}
            busyThreads={this.state.busyThreads}
            emptyMessage={this.props.options.emptyMessage}
          />
          {this.getMoreButton()}
        </Container>
      </div>
    )
  }
}

function isIndex(props) {
  if (props.category.level || !misago.get("THREADS_ON_INDEX"))
    return false
  if (props.options.title) return false

  return true
}
