/* jshint ignore:start */
import React from 'react';
import MisagoMarkup from 'misago/components/misago-markup';
import escapeHtml from 'misago/utils/escape-html';

export default function(props) {
  if (props.post.content) {
    return <Default {...props} />;
  } else {
    return <Invalid {...props} />;
  }
}

export function Default(props) {
 return (
    <div className="post-body">
      <MisagoMarkup markup={props.post.content} />
    </div>
  );
}

export function Invalid(props) {
 return (
    <div className="post-body post-body-invalid">
      <p className="lead">{gettext("This post's contents cannot be displayed.")}</p>
      <p className="text-muted">{gettext("This error is caused by invalid post content manipulation.")}</p>
    </div>
  );
}