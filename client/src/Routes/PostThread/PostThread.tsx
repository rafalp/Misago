import { t } from "@lingui/macro"
import { I18n } from "@lingui/react"
import React, { Suspense } from "react"
import { useParams } from "react-router-dom"
import { useAuthContext } from "../../Context"
import RouteContainer from "../../UI/RouteContainer"
import { RouteGraphQLError } from "../../UI/RouteError"
import RouteLoader from "../../UI/RouteLoader"
import WindowTitle from "../../UI/WindowTitle"
import PostThreadAuthRequiredError from "./PostThreadAuthRequiredError"
import PostThreadForm from "./PostThreadForm"
import PostThreadPermissionDeniedError from "./PostThreadPermissionDeniedError"
import useCategoriesQuery from "./useCategoriesQuery"
import useValidCategories from "./useValidCategories"

interface IPostThreadRouteParams {
  id?: string
}

const PostThread: React.FC = () => {
  const params = useParams<IPostThreadRouteParams>()
  const user = useAuthContext()
  const { data, error, loading } = useCategoriesQuery()
  const categories = data ? data.categories : []
  const validCategories = useValidCategories(user, categories)

  if (!user) return <PostThreadAuthRequiredError />
  if (!data) {
    if (error) return <RouteGraphQLError error={error} />
    if (loading) return <RouteLoader />
  }
  if (!validCategories.length) return <PostThreadPermissionDeniedError />

  return (
    <Suspense fallback={<RouteLoader />}>
      <RouteContainer>
        <I18n>
          {({ i18n }) => (
            <WindowTitle title={i18n._(t("post_thread.title")`Post thread`)} />
          )}
        </I18n>
        <PostThreadForm
          category={params && params.id}
          categories={categories}
          validCategories={validCategories}
        />
      </RouteContainer>
    </Suspense>
  )
}

export default PostThread
