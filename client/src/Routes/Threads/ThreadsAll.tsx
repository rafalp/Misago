import { t } from "@lingui/macro"
import { I18n } from "@lingui/react"
import React from "react"
import { LoadMoreButton, RouteLoader, WindowTitle } from "../../UI"
import { ForumStatsContext, SettingsContext } from "../../Context"
import { ThreadsHeaderAll } from "./ThreadsHeader"
import ThreadsLayout from "./ThreadsLayout"
import ThreadsList from "./ThreadsList"
import ThreadsToolbar from "./ThreadsToolbar"
import useThreadsModeration from "./useThreadsModeration"
import { useThreadsQuery } from "./useThreadsQuery"
import useThreadsSelection from "./useThreadsSelection"

const ThreadsAll: React.FC = () => {
  const forumStats = React.useContext(ForumStatsContext)
  const settings = React.useContext(SettingsContext)
  const { data, error, loading, update, fetchMoreThreads } = useThreadsQuery()
  const { threads } = data || { threads: null }

  const selection = useThreadsSelection(threads?.items || [])
  const moderation = useThreadsModeration()

  if (!forumStats || !settings) return <RouteLoader />

  const isIndex = settings.forumIndexThreads

  return (
    <ThreadsLayout>
      <I18n>
        {({ i18n }) => {
          return (
            <>
              <WindowTitle
                index={isIndex}
                title={i18n._(t("threads.title")`Threads`)}
                alerts={update.threads}
              />
              <ThreadsHeaderAll settings={settings} stats={forumStats} />
              <ThreadsToolbar />
              <ThreadsList
                error={error}
                loading={loading}
                selectable={!!moderation}
                selection={selection}
                threads={threads}
                update={update}
              />
              <LoadMoreButton
                data={threads}
                loading={loading}
                onEvent={fetchMoreThreads}
              />
            </>
          )
        }}
      </I18n>
    </ThreadsLayout>
  )
}

export default ThreadsAll
