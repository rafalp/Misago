import React from "react"
import { Card, CardBanner, CardColorBand } from "../../../UI"
import { useThreadACL } from "../../../acl"
import { IThread } from "../Thread.types"
import { useThreadModeration } from "../ThreadModeration"
import ThreadHeaderBody from "./ThreadHeaderBody"
import ThreadHeaderTitleEditForm from "./ThreadHeaderTitleEditForm"

interface IThreadHeaderProps {
  thread: IThread
}

const ThreadHeader: React.FC<IThreadHeaderProps> = ({ thread }) => {
  const acl = useThreadACL(thread)
  const moderation = useThreadModeration(thread)

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
