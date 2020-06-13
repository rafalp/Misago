import React from "react"
import { Redirect } from "react-router-dom"
import {
  RouteContainer,
  RouteGraphQLError,
  RouteLoader,
  RouteNotFound,
  WindowTitle,
} from "../../UI"
import { useThreadACL } from "../../acl"
import * as urls from "../../urls"
import ThreadHeader from "./ThreadHeader"
import { useThreadModeration } from "./ThreadModeration"
import useThreadParams from "./useThreadParams"
import { useThreadQuery } from "./useThreadQuery"

const ThreadRoute: React.FC = () => {
  const { id, slug, page } = useThreadParams()
  const { data, loading, error } = useThreadQuery({ id, page })
  const { thread } = data || { thread: null }
  const acl = useThreadACL(thread)
  const moderation = useThreadModeration(thread)

  if (!data) {
    if (error) return <RouteGraphQLError error={error} />
    if (loading) return <RouteLoader />
  }

  if (!thread) return <RouteNotFound />
  if (thread.slug !== slug) {
    return <Redirect to={urls.thread({ id, page, slug: thread.slug })} />
  }

  return (
    <RouteContainer
      className={`route-thread route-thread-${thread.category.id}`}
    >
      <WindowTitle title={thread.title} parent={thread.category.name} />
      <ThreadHeader acl={acl} moderation={moderation} thread={thread} />
    </RouteContainer>
  )
}

export default ThreadRoute
