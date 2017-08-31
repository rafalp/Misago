// jshint ignore:start
import moment from 'moment';
import React from 'react';
import Avatar from 'misago/components/avatar';

export default function({ result }) {
  const { rank } = result;

  const detail = gettext("%(title)s, joined on %(joined_on)s");
  const title = result.title || rank.title || rank.name;

  return (
    <li>
      <a href={result.url} className="dropdown-search-user">
        <div className="media">
          <div className="media-left">
            <Avatar size={38} user={result} />
          </div>
          <div className="media-body">
            <h5 className="media-heading">{result.username}</h5>
            <small>
              {interpolate(detail, {
                title,
                joined_on: moment(result.joined_on).format('LL')
              }, true)}
            </small>
          </div>
        </div>
      </a>
    </li>
  );
}