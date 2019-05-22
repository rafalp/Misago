import React from "react"
import Button from "misago/components/button"
import {
  compareGlobalWeight,
  compareWeight
} from "misago/components/threads/compare"
import Container from "misago/components/threads/container"
import Header from "misago/components/threads/header"
import {
  diffThreads,
  getModerationActions,
  getPageTitle,
  getTitle
} from "misago/components/threads/utils"
import ThreadsList from "misago/components/threads-list"
import ThreadsListEmpty from "misago/components/threads/list-empty"
import WithDropdown from "misago/components/with-dropdown"
import misago from "misago/index"
import * as select from "misago/reducers/selection"
import { append, deleteThread, hydrate, patch } from "misago/reducers/threads"
import ajax from "misago/services/ajax"
import polls from "misago/services/polls"
import snackbar from "misago/services/snackbar"
import store from "misago/services/store"
import title from "misago/services/page-title"
import * as sets from "misago/utils/sets"

export default class extends WithDropdown {
  constructor(props) {
    super(props)

    this.state = {
      isMounted: true,

      isLoaded: false,
      isBusy: false,

      diff: {
        results: []
      },

      moderation: [],
      busyThreads: [],

      dropdown: false,
      subcategories: [],
      
      next: 0,
    }

    let category = this.getCategory()

    if (misago.has("THREADS")) {
      this.initWithPreloadedData(category, misago.get("THREADS"))
    } else {
      this.initWithoutPreloadedData(category)
    }
  }

  getCategory() {
    if (!this.props.route.category.special_role) {
      return this.props.route.category.id
    } else {
      return null
    }
  }

  initWithPreloadedData(category, data) {
    this.state = Object.assign(this.state, {
      moderation: getModerationActions(data.results),
      subcategories: data.subcategories,
      next: data.next
    })

    this.startPolling(category)
  }

  initWithoutPreloadedData(category) {
    this.loadThreads(category)
  }

  loadThreads(category, next = 0) {
    ajax
      .get(
        this.props.options.api,
        {
          category: category,
          list: this.props.route.list.type,
          start: next || 0
        },
        "threads"
      )
      .then(
        data => {
          if (!this.state.isMounted) {
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

          this.startPolling(category)
        },
        rejection => {
          snackbar.apiError(rejection)
        }
      )
  }

  startPolling(category) {
    polls.start({
      poll: "threads",
      url: this.props.options.api,
      data: {
        category: category,
        list: this.props.route.list.type
      },
      frequency: 120 * 1000,
      update: this.pollResponse
    })
  }

  componentDidMount() {
    this.setPageTitle()

    if (misago.has("THREADS")) {
      // unlike in other components, routes are root components for threads
      // so we can't dispatch store action from constructor
      store.dispatch(hydrate(misago.pop("THREADS").results))

      this.setState({
        isLoaded: true
      })
    }

    store.dispatch(select.none())
  }

  componentWillUnmount() {
    this.state.isMounted = false
    polls.stop("threads")
  }

  getTitle() {
    if (this.props.options.title) {
      return this.props.options.title
    }

    return getTitle(this.props.route)
  }

  setPageTitle() {
    if (this.props.route.category.level || !misago.get("THREADS_ON_INDEX")) {
      title.set(getPageTitle(this.props.route))
    } else if (this.props.options.title) {
      title.set(this.props.options.title)
    } else {
      if (misago.get("SETTINGS").index_title) {
        document.title = misago.get("SETTINGS").index_title
      } else {
        document.title = misago.get("SETTINGS").forum_name
      }
    }
  }

  getSorting() {
    if (this.props.route.category.level) {
      return compareWeight
    } else {
      return compareGlobalWeight
    }
  }

  // AJAX

  loadMore = () => {
    this.setState({
      isBusy: true
    })

    this.loadThreads(this.getCategory(), this.state.next)
  }

  pollResponse = data => {
    this.setState({
      diff: Object.assign({}, data, {
        results: diffThreads(this.props.threads, data.results)
      })
    })
  }

  addThreads = threads => {
    store.dispatch(append(threads, this.getSorting()))
  }

  applyDiff = () => {
    this.addThreads(this.state.diff.results)

    this.setState(
      Object.assign({}, this.state.diff, {
        moderation: getModerationActions(store.getState().threads),

        diff: {
          results: []
        }
      })
    )
  }

  // Thread state utils

  freezeThread = thread => {
    this.setState(function(currentState) {
      return {
        busyThreads: sets.toggle(currentState.busyThreads, thread)
      }
    })
  }

  updateThread = thread => {
    store.dispatch(patch(thread, thread, this.getSorting()))
  }

  deleteThread = thread => {
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
    className += " page-threads-" + this.props.route.list.type
    if (this.props.route.category.css_class) {
      className += " page-threads-" + this.props.route.category.css_class
    }
    return className
  }

  render() {
    return (
      <div className={this.getClassName()}>
        <Header
          categories={this.props.route.categoriesMap}
          disabled={!this.state.isLoaded}
          startThread={this.props.options.startThread}
          threads={this.props.threads}
          title={this.getTitle()}
          toggleNav={this.toggleNav}
          route={this.props.route}
          user={this.props.user}
        />

        <Container
          api={this.props.options.api}
          route={this.props.route}
          subcategories={this.state.subcategories}
          user={this.props.user}
          pageLead={this.props.options.pageLead}
          threads={this.props.threads}
          threadsCount={this.state.count}
          moderation={this.state.moderation}
          selection={this.props.selection}
          busyThreads={this.state.busyThreads}
          addThreads={this.addThreads}
          freezeThread={this.freezeThread}
          deleteThread={this.deleteThread}
          updateThread={this.updateThread}
          isLoaded={this.state.isLoaded}
          isBusy={this.state.isBusy}
        >
          <ThreadsList
            category={this.props.route.category}
            categories={this.props.route.categoriesMap}
            list={this.props.route.list}
            selection={this.props.selection}
            threads={this.props.threads}
            diffSize={this.state.diff.results.length}
            applyDiff={this.applyDiff}
            showOptions={!!this.props.user.id}
            isLoaded={this.state.isLoaded}
            busyThreads={this.state.busyThreads}
          >
            <ThreadsListEmpty
              category={this.props.route.category}
              emptyMessage={this.props.options.emptyMessage}
              list={this.props.route.list}
            />
          </ThreadsList>

          {this.getMoreButton()}
        </Container>
      </div>
    )
  }
}
