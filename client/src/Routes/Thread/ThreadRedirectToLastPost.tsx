import React from "react"
import { Redirect, useParams } from "react-router-dom"
import { RouteGraphQLError, RouteLoader, RouteNotFound } from "../../UI"
import useThreadLastPostUrlQuery from "./useThreadLastPostUrlQuery"

interface IThreadLastPostRouteParams {
  id: string
  slug: string
}

const ThreadRedirectToLastPost: React.FC = () => {
  const { id } = useParams<IThreadLastPostRouteParams>()
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
