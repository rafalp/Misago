import React from "react"
import { PostingForm } from "../../../UI/PostingForm"
import ThreadReplyForm from "./ThreadReplyForm"
import { useThreadReplyContext } from "./ThreadReplyContext"
import ThreadReplySpacer from "./ThreadReplySpacer"

interface IThreadReplyProps {
  threadId: string
}

const ThreadReply: React.FC<IThreadReplyProps> = ({ threadId }) => {
  const context = useThreadReplyContext()
  const [height, setHeight] = React.useState(0)
  const element = React.useRef<HTMLDivElement | null>(null)
  const { isActive, fullscreen, minimized } = context || {}

  React.useLayoutEffect(() => {
    const interval = window.setInterval(() => {
      if (isActive && element.current) {
        setHeight(element.current.offsetHeight || 0)
      }
    }, 750)

    return () => window.clearInterval(interval)
  }, [setHeight, isActive, element])

  return (
    <>
      <ThreadReplySpacer
        height={isActive && !fullscreen && !minimized ? height : 0}
      />
      <PostingForm
        fullscreen={fullscreen}
        minimized={minimized}
        element={element}
        show={isActive}
      >
        <ThreadReplyForm threadId={threadId} />
      </PostingForm>
    </>
  )
}

export default React.memo(ThreadReply)
