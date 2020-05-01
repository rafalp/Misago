import { t } from "@lingui/macro"
import { I18n } from "@lingui/react"
import React from "react"
import { LoadMoreButton, RouteLoader, WindowTitle } from "../../UI"
import { ForumStatsContext, SettingsContext } from "../../Context"
import { ThreadsHeaderAll } from "./ThreadsHeader"
import { IThreadsProps } from "./Threads.types"
import ThreadsLayout from "./ThreadsLayout"
import ThreadsList from "./ThreadsList"
import ThreadsToolbar from "./ThreadsToolbar"
import { useThreadsQuery } from "./useThreadsQuery"

const ThreadsAll: React.FC<IThreadsProps> = ({ openCategoryPicker }) => {
  const forumStats = React.useContext(ForumStatsContext)
  const settings = React.useContext(SettingsContext)
  const { data, error, loading, update, fetchMoreThreads } = useThreadsQuery()

  if (!forumStats || !settings) return <RouteLoader />

  const isIndex = settings.forumIndexThreads
  const { threads } = data || { threads: null }

  return (
    <ThreadsLayout openCategoryPicker={openCategoryPicker}>
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
