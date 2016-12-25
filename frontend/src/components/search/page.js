// jshint ignore:start
import React from 'react';
import SearchForm from './form';
import SideNav from './sidenav';

export default function(props) {
  return (
    <div className="page page-search">
      <SearchForm
        provider={props.provider}
        search={props.search}
      />
      <div className="container">
        <div className="row">
          <div className="col-md-3">
            <SideNav providers={props.search.providers} />
          </div>
          <div className="col-md-9">
            {props.children}
            <SearchTime
              provider={props.provider}
              search={props.search}
            />
          </div>
        </div>
      </div>
    </div>
  )
}

export function SearchTime(props) {
  let time = null;
  props.search.providers.forEach((p) => {
    if (p.id === props.provider.id) {
      time = p.time;
    }
  });

  if (time === null) return null;

  const copy = gettext("Search took %(time)s s to complete");

  return (
    <footer className="search-footer">
      <p>
        {interpolate(copy, {time}, true)}
      </p>
    </footer>
  );
}