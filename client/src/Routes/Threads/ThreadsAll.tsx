import { t } from "@lingui/macro"
import { I18n } from "@lingui/react"
import React from "react"
import { LoadMoreButton, RouteLoader, WindowTitle } from "../../UI"
import { useForumStatsContext, useSettingsContext } from "../../Context"
import { ThreadsHeaderAll } from "./ThreadsHeader"
import ThreadsLayout from "./ThreadsLayout"
import ThreadsList from "./ThreadsList"
import { useThreadsModeration } from "./ThreadsModeration"
import ThreadsToolbar from "./ThreadsToolbar"
import { useThreadsQuery } from "./useThreadsQuery"
import useThreadsSelection from "./useThreadsSelection"

const ThreadsAll: React.FC = () => {
  const forumStats = useForumStatsContext()
  const settings = useSettingsContext()
  const { data, error, loading, update, fetchMoreThreads } = useThreadsQuery()
  const { threads } = data || { threads: null }

  const selection = useThreadsSelection(threads?.items || [])
  const moderation = useThreadsModeration(selection.selected)

  if (!forumStats || !settings) return <RouteLoader />

  const isIndex = settings.forumIndexThreads

  return (
    <ThreadsLayout>
      <I18n>
        {({ i18n }) => (
          <WindowTitle
            index={isIndex}
            title={i18n._(t("threads.title")`Threads`)}
            alerts={update.threads}
          />
        )}
      </I18n>
      <ThreadsHeaderAll settings={settings} stats={forumStats} />
      <ThreadsToolbar moderation={moderation} selection={selection} />
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
    </ThreadsLayout>
  )
}

export default ThreadsAll
