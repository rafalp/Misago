import React from "react"
import PageContainer from "../PageContainer"
import SearchForm from "./form"
import SideNav from "./sidenav"

export default function (props) {
  return (
    <div className="page page-search">
      <SearchForm provider={props.provider} search={props.search} />
      <PageContainer>
        <div className="row">
          <div className="col-md-3">
            <SideNav providers={props.search.providers} />
          </div>
          <div className="col-md-9">
            {props.children}
            <SearchTime provider={props.provider} search={props.search} />
          </div>
        </div>
      </PageContainer>
    </div>
  )
}

export function SearchTime(props) {
  let time = null
  props.search.providers.forEach((p) => {
    if (p.id === props.provider.id) {
      time = p.time
    }
  })

  if (time === null) return null

  const copy = pgettext("search time", "Search took %(time)s s")

  return (
    <footer className="search-footer">
      <p>{interpolate(copy, { time }, true)}</p>
    </footer>
  )
}
