import { t } from "@lingui/macro"
import React from "react"
import LoadMoreButton from "../../UI/LoadMoreButton"
import RouteLoader from "../../UI/RouteLoader"
import WindowTitle from "../../UI/WindowTitle"
import { useForumStatsContext, useSettingsContext } from "../../Context"
import { ThreadsHeaderAll } from "./ThreadsHeader"
import ThreadsLayout from "./ThreadsLayout"
import ThreadsList from "./ThreadsList"
import {
  ThreadsModerationMenu,
  useThreadsModeration,
} from "./ThreadsModeration"
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
    <ThreadsLayout className="route-threads">
      <WindowTitle
        index={isIndex}
        title={t({ id: "threads.title", message: "Threads" })}
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
      <ThreadsModerationMenu moderation={moderation} selection={selection} />
    </ThreadsLayout>
  )
}

export default ThreadsAll
