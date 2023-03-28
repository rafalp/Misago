import React from "react"
import { Link } from "react-router-dom"

const RankUsersPagination = ({ baseUrl, users }) => (
  <div className="misago-pagination">
    {users.isLoaded && users.first ? (
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
    {users.isLoaded && users.previous ? (
      <Link
        className="btn btn-default btn-outline btn-icon"
        to={baseUrl + (users.previous > 1 ? users.previous + "/" : "")}
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
    {users.isLoaded && users.next ? (
      <Link
        className="btn btn-default btn-outline btn-icon"
        to={baseUrl + users.next + "/"}
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
    {users.isLoaded && users.last ? (
      <Link
        className="btn btn-default btn-outline btn-icon"
        to={baseUrl + users.last + "/"}
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

export default RankUsersPagination
