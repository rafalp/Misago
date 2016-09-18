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
  if (props.posts.pages > 1) {
    return <ul className="pagination">
      <FirstPage {...props} />
      <PreviousPage {...props} />
      <NextPage {...props} />
      <LastPage {...props} />
    </ul>;
  } else {
    return null;
  }
}

export function FirstPage(props) {
  if (props.posts.isLoaded && props.posts.first) {
    return <li>
      <Link to={props.thread.url.index} title={gettext("Go to first page")}>
        <span className="material-icon">first_page</span>
      </Link>
    </li>;
  } else {
    return <li className="disabled">
      <span title={gettext("Go to first page")}>
        <span className="material-icon">first_page</span>
      </span>
    </li>;
  }
}

export function PreviousPage(props) {
  if (props.posts.isLoaded && props.posts.page > 1) {
    let previousUrl = '';
    if (props.posts.previous) {
      previousUrl = props.posts.previous + '/';
    }

    return <li>
      <Link to={props.thread.url.index + previousUrl} title={gettext("Go to previous page")}>
        <span className="material-icon">chevron_left</span>
      </Link>
    </li>;
  } else {
    return <li className="disabled">
      <span title={gettext("Go to previous page")}>
        <span className="material-icon">chevron_left</span>
      </span>
    </li>;
  }
}

export function NextPage(props) {
  if (props.posts.isLoaded && props.posts.more) {
    let nextUrl = '';
    if (props.posts.next) {
      nextUrl = props.posts.next + '/';
    }

    return <li>
      <Link to={props.thread.url.index + nextUrl} title={gettext("Go to next page")}>
        <span className="material-icon">chevron_right</span>
      </Link>
    </li>;
  } else {
    return <li className="disabled">
      <span title={gettext("Go to next page")}>
        <span className="material-icon">chevron_right</span>
      </span>
    </li>;
  }
}

export function LastPage(props) {
  if (props.posts.isLoaded && props.posts.last) {
    return <li>
      <Link to={props.thread.url.index + props.posts.last + '/'} title={gettext("Go to last page")}>
        <span className="material-icon">last_page</span>
      </Link>
    </li>;
  } else {
    return <li className="disabled">
      <span title={gettext("Go to last page")}>
        <span className="material-icon">last_page</span>
      </span>
    </li>;
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