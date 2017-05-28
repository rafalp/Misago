// jshint ignore:start
import React from 'react';
import ListItem from './list-item';

export default function({ category }) {
  let className = 'list-group list-group-category';
  if (category.css_class) {
    className += ' list-group-category-has-flavor';
    className += ' list-group-category-' + category.css_class;
  }

  return (
    <ul className={className}>
      <ListItem
        category={category}
        isFirst={true}
      />
      {category.subcategories.map((category) => {
        return (
          <ListItem
            category={category}
            isFirst={false}
            key={category.id}
          />
        );
      })}
    </ul>
  );
}