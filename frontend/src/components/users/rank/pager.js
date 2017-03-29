/* jshint ignore:start */
import React from 'react';
import { Link } from 'react-router';
import resetScroll from 'misago/utils/reset-scroll';

export default function(props) {
  if (props.pages === 1) return null;

  return (
    <div className="row row-toolbar">
      <div className="col-xs-12 text-center visible-xs-block">
        <More more={props.more} />
        <div className="toolbar-vertical-spacer" />
      </div>
      <div className="col-md-7">
        <div className="row">
          <div className="col-sm-4 col-md-5">
            <Pager {...props} />
          </div>
          <div className="col-sm-8 col-md-7 hidden-xs">
            <More more={props.more} />
          </div>
        </div>
      </div>
    </div>
  );
}

export function Pager(props) {
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
  if (props.isLoaded && props.first) {
    return (
      <Link
        className="btn btn-default btn-block btn-icon"
        onClick={resetScroll}
        to={props.baseUrl}
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
  if (props.isLoaded && props.page > 1) {
    let previousUrl = '';
    if (props.previous) {
      previousUrl = props.previous + '/';
    }

    return (
      <Link
        className="btn btn-default btn-block btn-icon"
        onClick={resetScroll}
        to={props.baseUrl + previousUrl}
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
  if (props.isLoaded && props.more) {
    let nextUrl = '';
    if (props.next) {
      nextUrl = props.next + '/';
    }

    return (
      <Link
        className="btn btn-default btn-block btn-icon"
        onClick={resetScroll}
        to={props.baseUrl + nextUrl}
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
  if (props.isLoaded && props.last) {
    return (
      <Link
        className="btn btn-default btn-block btn-icon"
        onClick={resetScroll}
        to={props.baseUrl + props.last + '/'}
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
      "There is %(more)s more member with this role.",
      "There are %(more)s more members with this role.",
      props.more);
    message = interpolate(message, {'more': props.more}, true);
  } else {
    message = gettext("There are no more members with this role.");
  }

  return <p>{message}</p>;
}