import React from "react"
import { Redirect, useParams } from "react-router-dom"
import { RouteGraphQLError, RouteNotFound } from "../../UI/RouteError"
import RouteLoader from "../../UI/RouteLoader"
import usePostUrlQuery from "./usePostUrlQuery"

const RedirectToPost: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const { data, loading, error } = usePostUrlQuery({ id })

  if (!data) {
    if (error) return <RouteGraphQLError error={error} />
    if (loading) return <RouteLoader />
  }

  if (data?.post?.url) {
    return <Redirect to={data.post.url} />
  }

  return <RouteNotFound />
}

export default RedirectToPost
