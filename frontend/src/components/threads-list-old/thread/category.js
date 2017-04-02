/* jshint ignore:start */
import React from 'react';
import { Link } from 'react-router';

export default function(props) {
  const { category, list } = props

  const url = category.absolute_url + list.path

  let className = 'thread-category';
  if (category.css_class) {
    className += ' thread-category-' + category.css_class;
  }

  return (
    <Link to={url} className={className}>
      {category.name}
    </Link>
  );
}