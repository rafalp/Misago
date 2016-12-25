// jshint ignore:start
import React from 'react';
import Button from 'misago/components/button';
import MisagoMarkup from 'misago/components/misago-markup';
import { update as updatePosts, append as appendPosts } from 'misago/reducers/posts';
import { updateProvider } from 'misago/reducers/search';
import ajax from 'misago/services/ajax';
import snackbar from 'misago/services/snackbar';
import store from 'misago/services/store';

export default function(props) {
  return (
    <div>
      <ul className="list-group">
        {props.results.map((post) => {
          return (
            <Post
              key={post.id}
              {...post}
            />
          );
        })}
      </ul>
      <LoadMore {...props} />
    </div>
  );
}

export function Post(props) {
  return (
    <li className="list-group-item">
      <h4>
        <a href={props.url.index} className="item-title">
          {props.thread.title}
        </a>
      </h4>

      <PostContent content={props.content} />

      <ul className="list-inline list-unstyled">
        <Poster {...props} />
        <Timestamp {...props} />
        <Category {...props.category} />
      </ul>
    </li>
  );
}

export function PostContent(props) {
  if (!props.content) return null;

  return (
    <MisagoMarkup markup={props.content} />
  );
}

export function Category(props) {
  return (
    <li>
      <a href={props.absolute_url}>
        {props.name}
      </a>
    </li>
  );
}

export function Poster(props) {
  if (!props.poster) {
    return (
      <li>
        {props.poster_namer}
      </li>
    );
  }

  return (
    <li>
      <a href={props.poster.url} className="item-title">
        {props.poster.username}
      </a>
    </li>
  );
}

export function Timestamp(props) {
  const tooltip = interpolate(gettext("posted %(posted_on)s"), {
    'posted_on': props.posted_on.format('LL, LT')
  }, true);

  const message = interpolate(gettext("posted %(posted_on)s"), {
    'posted_on': props.posted_on.fromNow()
  }, true);

  return (
    <li>
      <abbr title={tooltip}>
        {message}
      </abbr>
    </li>
  );
}

export class LoadMore extends React.Component {
  onClick = () => {
    store.dispatch(updatePosts({
      isBusy: true
    }));

    ajax.get(this.props.provider.api, {
      q: this.props.query,
      page: this.props.next
    }).then((providers) => {
      providers.forEach((provider) => {
        if (provider.id !== 'threads') return;
        store.dispatch(appendPosts(provider.results));
        store.dispatch(updateProvider(provider));
      });

      store.dispatch(updatePosts({
        isBusy: false
      }));
    }, (rejection) => {
      snackbar.apiError(rejection);

      store.dispatch(updatePosts({
        isBusy: false
      }));
    });
  };

  render() {
    if (!this.props.more) return null;

    return (
      <div className="pager-more">
        <Button
          loading={this.props.isBusy}
          onClick={this.onClick}
        >
          {gettext("Show more")}
        </Button>
      </div>
    );
  }
}