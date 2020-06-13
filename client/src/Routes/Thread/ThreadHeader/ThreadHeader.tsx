import React from "react"
import { Card, CardBanner, CardColorBand } from "../../../UI"
import { IThread, IThreadModeration } from "../Thread.types"
import ThreadHeaderBody from "./ThreadHeaderBody"
import ThreadHeaderTitleEditForm from "./ThreadHeaderTitleEditForm"

interface IThreadHeaderProps {
  acl: { edit: boolean }
  moderation: IThreadModeration | null
  thread: IThread
}

const ThreadHeader: React.FC<IThreadHeaderProps> = ({
  acl,
  moderation,
  thread,
}) => {
  const [edit, setEdit] = React.useState(false)
  const editThread = () => setEdit(true)

  return (
    <Card className="thread-header">
      {thread.category.color && (
        <CardColorBand color={thread.category.color} />
      )}
      {thread.category.banner && (
        <CardBanner {...thread.category.banner.full} desktop />
      )}
      {thread.category.banner && (
        <CardBanner {...thread.category.banner.half} mobile />
      )}
      {edit ? (
        <ThreadHeaderTitleEditForm
          thread={thread}
          close={() => setEdit(false)}
        />
      ) : (
        <ThreadHeaderBody
          acl={acl}
          editThread={editThread}
          moderation={moderation}
          thread={thread}
        />
      )}
    </Card>
  )
}

export default React.memo(ThreadHeader)
