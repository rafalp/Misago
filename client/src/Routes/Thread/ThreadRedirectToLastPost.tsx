import React from "react"
import { Redirect, useParams } from "react-router-dom"
import { RouteGraphQLError, RouteNotFound } from "../../UI/RouteError"
import RouteLoader from "../../UI/RouteLoader"
import useThreadLastPostUrlQuery from "./useThreadLastPostUrlQuery"

interface ThreadLastPostRouteParams {
  id: string
  slug: string
}

const ThreadRedirectToLastPost: React.FC = () => {
  const { id } = useParams<ThreadLastPostRouteParams>()
  const { data, loading, error } = useThreadLastPostUrlQuery({ id })

  if (!data) {
    if (error) return <RouteGraphQLError error={error} />
    if (loading) return <RouteLoader />
  }

  if (data?.thread?.lastPostUrl) {
    return <Redirect to={data.thread.lastPostUrl} />
  }

  return <RouteNotFound />
}

export default ThreadRedirectToLastPost
