import React from "react"
import { Card, CardBanner, CardColorBand } from "../../../UI/Card"
import { Thread } from "../Thread.types"
import ThreadHeaderBody from "./ThreadHeaderBody"
import ThreadHeaderTitleEditForm from "./ThreadHeaderTitleEditForm"
import useThreadAcl from "./useThreadAcl"

interface ThreadHeaderProps {
  thread: Thread
}

const ThreadHeader: React.FC<ThreadHeaderProps> = ({ thread }) => {
  const acl = useThreadAcl(thread)

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
        <ThreadHeaderBody acl={acl} editThread={editThread} thread={thread} />
      )}
    </Card>
  )
}

export default React.memo(ThreadHeader)
