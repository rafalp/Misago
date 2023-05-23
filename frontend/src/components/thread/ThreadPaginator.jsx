import React from "react"
import { Link, withRouter } from "react-router"
import { Dropdown } from "../Dropdown"

const ThreadPaginator = ({ router, baseUrl, posts, scrollToTop }) => (
  <div className="thread-paginator">
    {posts.isLoaded && posts.first ? (
      <Link
        className="btn btn-default btn-outline btn-icon"
        to={baseUrl}
        title={pgettext("paginator", "Go to first page")}
        onClick={scrollToTop ? resetScroll : null}
      >
        <span className="material-icon">first_page</span>
      </Link>
    ) : (
      <button
        className="btn btn-default btn-outline btn-icon"
        title={pgettext("paginator", "Go to first page")}
        type="button"
        disabled
      >
        <span className="material-icon">first_page</span>
      </button>
    )}
    {posts.isLoaded && posts.previous ? (
      <Link
        className="btn btn-default btn-outline btn-icon"
        to={baseUrl + (posts.previous > 1 ? posts.previous + "/" : "")}
        title={pgettext("paginator", "Go to previous page")}
        onClick={scrollToTop ? resetScroll : null}
      >
        <span className="material-icon">chevron_left</span>
      </Link>
    ) : (
      <button
        className="btn btn-default btn-outline btn-icon"
        title={pgettext("paginator", "Go to previous page")}
        type="button"
        disabled
      >
        <span className="material-icon">chevron_left</span>
      </button>
    )}
    <Dropdown
      toggle={({ aria, toggle }) => (
        <button
          {...aria}
          className="btn btn-default btn-block btn-outline"
          type="button"
          disabled={!posts.isLoaded}
          onClick={toggle}
        >
          {getLabel(posts.page, posts.pages)}
        </button>
      )}
      onOpen={(dropdown) => {
        dropdown.querySelector("input").focus()
      }}
    >
      {({ close }) => (
        <form
          className="thread-paginator-form"
          onSubmit={(event) => {
            if (posts.isLoaded) {
              const formData = new FormData(event.target)
              const page = parseInt(formData.get("page"))

              if (
                page &&
                page != posts.page &&
                page >= 1 &&
                page <= posts.pages
              ) {
                const url = page > 1 ? baseUrl + page + "/" : baseUrl
                router.push({ pathname: url })
              }
            }

            event.preventDefault()
            close()

            if (scrollToTop) {
              resetScroll()
            }
          }}
        >
          <input
            className="form-control"
            name="page"
            type="number"
            min={1}
            max={posts.pages}
            placeholder={pgettext("paginator input", "Page")}
            disabled={!posts.isLoaded}
          />
          <button
            className="btn btn-primary"
            type="submit"
            disabled={!posts.isLoaded}
          >
            {pgettext("paginator", "Go")}
          </button>
        </form>
      )}
    </Dropdown>
    {posts.isLoaded && posts.next ? (
      <Link
        className="btn btn-default btn-outline btn-icon"
        to={baseUrl + posts.next + "/"}
        title={pgettext("paginator", "Go to next page")}
        onClick={scrollToTop ? resetScroll : null}
      >
        <span className="material-icon">chevron_right</span>
      </Link>
    ) : (
      <button
        className="btn btn-default btn-outline btn-icon"
        title={pgettext("paginator", "Go to next page")}
        type="button"
        disabled
      >
        <span className="material-icon">chevron_right</span>
      </button>
    )}
    {posts.isLoaded && posts.last ? (
      <Link
        className="btn btn-default btn-outline btn-icon"
        to={baseUrl + posts.last + "/"}
        title={pgettext("paginator", "Go to last page")}
        onClick={scrollToTop ? resetScroll : null}
      >
        <span className="material-icon">last_page</span>
      </Link>
    ) : (
      <button
        className="btn btn-default btn-outline btn-icon"
        title={pgettext("paginator", "Go to last page")}
        type="button"
        disabled
      >
        <span className="material-icon">last_page</span>
      </button>
    )}
  </div>
)

function getLabel(page, pages) {
  return pgettext("paginator", "Page %(page)s of %(pages)s")
    .replace("%(page)s", page)
    .replace("%(pages)s", pages)
}

function resetScroll() {
  window.scrollTo(0, 0)
}

const ThreadPaginatorConnected = withRouter(ThreadPaginator)

export default ThreadPaginatorConnected
