import React from "react"
import { Link } from "react-router"

const ThreadPagination = ({ baseUrl, posts }) => (
  <div className="misago-pagination">
    {posts.isLoaded && posts.first ? (
      <Link
        className="btn btn-default btn-outline btn-icon"
        to={baseUrl}
        title={gettext("Go to first page")}
      >
        <span className="material-icon">first_page</span>
      </Link>
    ) : (
      <button
        className="btn btn-default btn-outline btn-icon"
        title={gettext("Go to first page")}
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
        title={gettext("Go to previous page")}
      >
        <span className="material-icon">chevron_left</span>
      </Link>
    ) : (
      <button
        className="btn btn-default btn-outline btn-icon"
        title={gettext("Go to previous page")}
        type="button"
        disabled
      >
        <span className="material-icon">chevron_left</span>
      </button>
    )}
    {posts.isLoaded && posts.next ? (
      <Link
        className="btn btn-default btn-outline btn-icon"
        to={baseUrl + posts.next + "/"}
        title={gettext("Go to next page")}
      >
        <span className="material-icon">chevron_right</span>
      </Link>
    ) : (
      <button
        className="btn btn-default btn-outline btn-icon"
        title={gettext("Go to next page")}
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
        title={gettext("Go to last page")}
      >
        <span className="material-icon">last_page</span>
      </Link>
    ) : (
      <button
        className="btn btn-default btn-outline btn-icon"
        title={gettext("Go to last page")}
        type="button"
        disabled
      >
        <span className="material-icon">last_page</span>
      </button>
    )}
  </div>
)

export default ThreadPagination
