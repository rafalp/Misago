import React from "react"
import SearchPage from "../page"
import UsersList from "misago/components/users-list"

export default function (props) {
  return (
    <SearchPage provider={props.route.provider} search={props.search}>
      <Blankslate
        loading={props.search.isLoading}
        query={props.search.query}
        users={props.users}
      >
        <UsersList
          cols={3}
          isReady={!props.search.isLoading}
          users={props.users}
        />
      </Blankslate>
    </SearchPage>
  )
}

export function Blankslate({ children, loading, query, users }) {
  if (users.length) return children

  if (query.length) {
    return (
      <p className="lead">
        {loading
          ? pgettext("search users", "Loading results...")
          : pgettext(
              "search users",
              "No users matching search query have been found."
            )}
      </p>
    )
  }

  return (
    <p className="lead">
      {pgettext(
        "search users",
        "Enter at least two characters to search users."
      )}
    </p>
  )
}
