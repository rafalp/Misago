import { t } from "@lingui/macro"
import { I18n } from "@lingui/react"
import React from "react"
import { Link } from "react-router-dom"
import {
  CategoriesNav,
  Layout,
  LayoutMain,
  LayoutSide,
  RouteContainer,
  RouteGraphQLError,
  RouteLoader,
  WindowTitle,
} from "../../UI"
import { SettingsContext } from "../../Context"
import * as urls from "../../urls"
import { HeaderAllThreads } from "./Header"
import { MobileCategoryNavButton } from "./MobileCategoryNav"
import { IThreadsProps } from "./Threads.types"
import { useThreadsQuery } from "./useThreadsQuery"

const ThreadsAll: React.FC<IThreadsProps> = ({
  openCategoryPicker,
}) => {
  const settings = React.useContext(SettingsContext)
  const { data, error, loading } = useThreadsQuery()

  if (!data && error) return <RouteGraphQLError error={error} />
  if (!data || !settings || loading) return <RouteLoader />

  const isIndex = settings.forumIndexThreads
  const { threads } = data

  return (
    <RouteContainer>
      <Layout>
        <LayoutSide>
          <CategoriesNav />
        </LayoutSide>
        <LayoutMain>
          <I18n>
            {({ i18n }) => {
              return (
                <>
                  <WindowTitle
                    index={isIndex}
                    title={i18n._(t("threads.title")`Threads`)}
                  />
                  <MobileCategoryNavButton onClick={() => openCategoryPicker()} />
                  <HeaderAllThreads settings={settings} />
                  <ul>
                    {threads.items.map((thread) => (
                      <li key={thread.id}>
                        <strong>
                          <Link to={urls.thread(thread)}>{thread.title}</Link>
                        </strong>
                        <ul className="list-inline">
                          {thread.category.parent && (
                            <li className="list-inline-item">
                              <Link
                                to={urls.category(thread.category.parent)}
                                style={{
                                  borderLeft: `4px solid ${thread.category.parent.color}`,
                                }}
                              >
                                {thread.category.parent.name}
                              </Link>
                            </li>
                          )}
                          <li className="list-inline-item">
                            <Link
                              to={urls.category(thread.category)}
                              style={{
                                borderLeft: `4px solid ${thread.category.color}`,
                              }}
                            >
                              {thread.category.name}
                            </Link>
                          </li>
                        </ul>
                      </li>
                    ))}
                  </ul>
                </>
              )
            }}
          </I18n>
        </LayoutMain>
      </Layout>
    </RouteContainer>
  )
}

export default ThreadsAll
