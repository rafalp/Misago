// jshint ignore:start
import React from 'react';
import Description from './description';
import Icon from './icon';

export default function({ category }) {
  return (
    <div className="col-xs-12 col-sm-6 col-md-6 category-main">
      <div className="media">
        <div className="media-left">
          <Icon category={category} />
        </div>
        <div className="media-body">
          <h4 className="media-heading">
            <a href={category.absolute_url}>
              {category.name}
            </a>
          </h4>
          <Description category={category} />
        </div>
      </div>
    </div>
  );
}