// jshint ignore:start
import React from 'react';
import { Link } from 'react-router';
import Li from 'misago/components/li';

export default function({baseUrl, list, lists}) {
  if (lists.length < 2) return null;

  return (
    <div className="page-tabs">
      <div className="container">
        <ul className="nav nav-pills">
          {lists.map((item) => {
            return (
              <Li
                isControlled={true}
                isActive={item.path === list.path}
                key={baseUrl + item.path}
              >
                <Link to={baseUrl + item.path}>
                  {item.name}
                </Link>
              </Li>
            );
          })}
        </ul>
      </div>
    </div>
  );
}