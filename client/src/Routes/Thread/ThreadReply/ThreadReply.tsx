import React from "react"
import { useAuthContext } from "../../../Context"
import ThreadReplyForm from "./ThreadReplyForm"

interface IThreadReplyProps {
  categoryId: string
  categoryIsClosed: boolean
  threadId: string
  threadIsClosed: boolean
}

const ThreadReply: React.FC<IThreadReplyProps> = ({
  categoryId,
  categoryIsClosed,
  threadId,
  threadIsClosed,
}) => {
  const user = useAuthContext()

  if (user && !user.isModerator) {
    if (categoryIsClosed) {
      return <div id="thread-reply">CATEGORY IS CLOSED</div>
    }

    if (threadIsClosed) {
      return <div id="thread-reply">THREAD IS CLOSED</div>
    }
  }

  if (!user) {
    return <div id="thread-reply">LOGIN TO REPLY THREADS</div>
  }

  return (
    <div id="thread-reply">
      <ThreadReplyForm threadId={threadId} />
    </div>
  )
}

export default React.memo(ThreadReply)
