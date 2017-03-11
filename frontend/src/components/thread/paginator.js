/* jshint ignore:start */
import React from 'react';
import { Link } from 'react-router'; // jshint ignore:line

export default function(props) {
  return <nav className="misago-pagination pull-left">
    <Pager {...props} />
    <More more={props.posts.more} />
  </nav>;
}

export function Pager(props) {
  if (props.posts.pages < 2) return null;

  return (
    <div className="row row-paginator">
      <div className="col-xs-3">
        <FirstPage {...props} />
      </div>
      <div className="col-xs-3">
        <PreviousPage {...props} />
      </div>
      <div className="col-xs-3">
        <NextPage {...props} />
      </div>
      <div className="col-xs-3">
        <LastPage {...props} />
      </div>
    </div>
  );
}

export function FirstPage(props) {
  if (props.posts.isLoaded && props.posts.first) {
    return (
      <Link
        className="btn btn-default btn-block btn-icon"
        to={props.thread.url.index}
        title={gettext("Go to first page")}
      >
        <span className="material-icon">first_page</span>
      </Link>
    );
  } else {
    return (
      <span
        className="btn btn-default btn-block btn-icon disabled"
        title={gettext("Go to first page")}
      >
        <span className="material-icon">first_page</span>
      </span>
    );
  }
}

export function PreviousPage(props) {
  if (props.posts.isLoaded && props.posts.page > 1) {
    let previousUrl = '';
    if (props.posts.previous) {
      previousUrl = props.posts.previous + '/';
    }

    return (
      <Link
        className="btn btn-default btn-block btn-icon"
        to={props.thread.url.index + previousUrl}
        title={gettext("Go to previous page")}
      >
        <span className="material-icon">chevron_left</span>
      </Link>
    );
  } else {
    return (
      <span
        className="btn btn-default btn-block btn-icon disabled"
        title={gettext("Go to previous page")}
      >
        <span className="material-icon">chevron_left</span>
      </span>
    );
  }
}

export function NextPage(props) {
  if (props.posts.isLoaded && props.posts.more) {
    let nextUrl = '';
    if (props.posts.next) {
      nextUrl = props.posts.next + '/';
    }

    return (
      <Link
        className="btn btn-default btn-block btn-icon"
        to={props.thread.url.index + nextUrl}
        title={gettext("Go to next page")}
      >
        <span className="material-icon">chevron_right</span>
      </Link>
    );
  } else {
    return (
      <span
        className="btn btn-default btn-block btn-icon disabled"
        title={gettext("Go to next page")}
      >
        <span className="material-icon">chevron_right</span>
      </span>
    );
  }
}

export function LastPage(props) {
  if (props.posts.isLoaded && props.posts.last) {
    return (
      <Link
        className="btn btn-default btn-block btn-icon"
        to={props.thread.url.index + props.posts.last + '/'}
        title={gettext("Go to last page")}
      >
        <span className="material-icon">last_page</span>
      </Link>
    );
  } else {
    return (
      <span
        className="btn btn-default btn-block btn-icon disabled"
        title={gettext("Go to last page")}
      >
        <span className="material-icon">last_page</span>
      </span>
    );
  }
}

export function More(props) {
  let message = null;
  if (props.more) {
    message = ngettext(
      "There is %(more)s more post in this thread.",
      "There are %(more)s more posts in this thread.",
      props.more);
    message = interpolate(message, {'more': props.more}, true);
  } else {
    message = gettext("There are no more posts in this thread.");
  }

  return <p>{message}</p>;
}