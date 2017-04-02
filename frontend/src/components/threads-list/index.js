/* jshint ignore:start */
import React from 'react';
import ListEmpty from 'misago/components/threads-list/list/empty';
import ListReady from 'misago/components/threads-list/list/ready';
import ListPreview from 'misago/components/threads-list/list/preview';

export default function(props) {
  if (!props.isLoaded) {
    return (
      <ListPreview />
    );
  }

  if (props.threads.length === 0) {
    return (
      <ListEmpty
        diffSize={props.diffSize}
        applyDiff={props.applyDiff}
      >
        {props.children}
      </ListEmpty>
    );
  }

  return (
    <ListReady
      activeCategory={props.category}
      categories={props.categories}
      list={props.list}
      threads={props.threads}

      diffSize={props.diffSize}
      applyDiff={props.applyDiff}

      showOptions={props.showOptions}
      selection={props.selection}

      busyThreads={props.busyThreads}
    />
  );
}