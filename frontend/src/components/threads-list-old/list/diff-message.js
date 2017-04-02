/* jshint ignore:start */
import React from 'react';

export default function(props) {
  const { diffSize, applyDiff } = props;

  if (diffSize === 0) return null;

  return (
    <li className="list-group-item threads-diff-message">
      <button
        type="button"
        className="btn btn-block btn-default"
        onClick={applyDiff}
      >
        <span className="material-icon">
          cached
        </span>
        <span className="diff-message">
          {getMessage(diffSize)}
        </span>
      </button>
    </li>
  );
}

export function getMessage(diffSize) {
  const message = ngettext(
    "There is %(threads)s new or updated thread. Click this message to show it.",
    "There are %(threads)s new or updated threads. Click this message to show them.",
    diffSize);

  return interpolate(message, {
    threads: diffSize
  }, true);
}