import React from "react"
import { Redirect } from "react-router-dom"
import RouteContainer from "../../UI/RouteContainer"
import { RouteGraphQLError, RouteNotFound } from "../../UI/RouteError"
import RouteLoader from "../../UI/RouteLoader"
import SectionLoader from "../../UI/SectionLoader"
import WindowTitle from "../../UI/WindowTitle"
import * as urls from "../../urls"
import ThreadBreadcrumbs from "./ThreadBreadcrumbs"
import ThreadHeader from "./ThreadHeader"
import { useThreadModeration } from "./ThreadModeration"
import {
  ThreadPostsModeration,
  useThreadPostsModeration,
} from "./ThreadPostsModeration"
import ThreadPost from "./ThreadPost"
import { ThreadReply, ThreadReplyProvider } from "./ThreadReply"
import { ThreadToolbarBottom, ThreadToolbarTop } from "./ThreadToolbar"
import useThreadParams from "./useThreadParams"
import usePostsSelection from "./usePostsSelection"
import { useThreadQuery } from "./useThreadQuery"

const ThreadPosts: React.FC = () => {
  const { id, slug, page } = useThreadParams()
  const { data, loading, error } = useThreadQuery({ id, page })
  const { thread } = data || { thread: null }

  const selection = usePostsSelection(
    thread && thread.posts.page ? thread.posts.page.items : []
  )
  const moderation = {
    thread: useThreadModeration(thread),
    posts: useThreadPostsModeration(thread, selection.selected, page),
  }

  if (!data) {
    if (error) return <RouteGraphQLError error={error} />
    if (loading) return <RouteLoader />
  }

  if (!thread) return <RouteNotFound />
  if (thread.id !== id) return <RouteLoader />
  if (page === 1 || thread.slug !== slug) {
    const newParams: { id: string; slug: string; page?: number } = { id, slug }
    if (page && page > 1) newParams.page = page
    return <Redirect to={urls.thread({ id, page, slug: thread.slug })} />
  }

  const posts = thread.posts
  if (!posts.page) {
    return (
      <Redirect
        to={urls.thread({
          id,
          slug: thread.slug,
          page: posts.pagination.pages,
        })}
      />
    )
  }

  const isClosed = thread.isClosed || thread.category.isClosed

  const pagination = {
    page: page || 1,
    pages: posts.pagination.pages,
    url: (page: number) => {
      return urls.thread({ ...thread, page })
    },
  }
  const toolbarProps = {
    isClosed,
    pagination,
    moderation: moderation.thread,
  }

  return (
    <RouteContainer
      className={`route-thread route-thread-${thread.category.id}`}
    >
      <WindowTitle title={thread.title} parent={thread.category.name} />
      <ThreadBreadcrumbs category={thread.category} />
      <ThreadHeader thread={thread} />
      <ThreadReplyProvider threadId={thread.id}>
        <ThreadToolbarTop {...toolbarProps} />
        <SectionLoader
          loading={loading || posts.page.number !== pagination.page}
        >
          {posts.page.items.map((post) => (
            <ThreadPost
              key={post.id}
              post={post}
              threadId={thread.id}
              threadSlug={thread.slug}
              page={page}
              isClosed={isClosed}
              isSelected={selection.selection[post.id]}
              toggleSelection={moderation.posts ? selection.toggle : null}
            />
          ))}
        </SectionLoader>
        <ThreadToolbarBottom {...toolbarProps} />
        <ThreadReply threadId={thread.id} />
      </ThreadReplyProvider>
      <ThreadPostsModeration
        moderation={moderation.posts}
        selection={selection}
      />
    </RouteContainer>
  )
}

export default ThreadPosts
