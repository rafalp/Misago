import React from "react"
import { Redirect } from "react-router-dom"
import {
  RouteContainer,
  RouteGraphQLError,
  RouteLoader,
  RouteNotFound,
  WindowTitle,
} from "../../UI"
import * as urls from "../../urls"
import ThreadHeader from "./ThreadHeader"
import ThreadPost from "./ThreadPost"
import { ThreadToolbarBottom, ThreadToolbarTop } from "./ThreadToolbar"
import useThreadParams from "./useThreadParams"
import { useThreadQuery } from "./useThreadQuery"

const ThreadRoute: React.FC = () => {
  const { id, slug, page } = useThreadParams()
  const { data, loading, error } = useThreadQuery({ id, page })
  const { thread } = data || { thread: null }

  if (!data) {
    if (error) return <RouteGraphQLError error={error} />
    if (loading) return <RouteLoader />
  }

  if (!thread) return <RouteNotFound />
  if (thread.id !== id) return <RouteLoader />
  if (thread.slug !== slug) {
    return <Redirect to={urls.thread({ id, page, slug: thread.slug })} />
  }
  if (!thread.posts) {
    return <Redirect to={urls.thread({ id, slug: thread.slug })} />
  }

  const posts = thread.posts
  const paginatorUrl = (page: number) => {
    return urls.thread({ ...thread, page })
  }

  return (
    <RouteContainer
      className={`route-thread route-thread-${thread.category.id}`}
    >
      <WindowTitle title={thread.title} parent={thread.category.name} />
      <ThreadHeader thread={thread} />
      <ThreadToolbarTop page={posts} paginatorUrl={paginatorUrl} />
      {loading && <RouteLoader />}
      {!loading &&
        posts.items.map((post) => <ThreadPost key={post.id} post={post} />)}
      <ThreadToolbarBottom page={posts} paginatorUrl={paginatorUrl} />
    </RouteContainer>
  )
}

export default ThreadRoute
