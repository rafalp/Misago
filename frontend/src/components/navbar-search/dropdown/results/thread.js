// jshint ignore:start
import moment from 'moment';
import React from 'react';

export default function({ result }) {
  const { poster, thread } = result;
  const footer = gettext("Posted by %(poster)s on %(posted_on)s in %(category)s.");

  return (
    <li>
      <a href={result.url.index} className="dropdown-search-thread">
        <h5>{thread.title}</h5>
        <small className="dropdown-search-post-content">
          {$(result.content).text()}
        </small>
        <small className="dropdown-search-post-footer">
          {interpolate(footer, {
            category: result.category.name,
            posted_on: moment(result.posted_on).format('LL'),
            poster: result.poster_name
          }, true)}
        </small>
      </a>
    </li>
  );
}