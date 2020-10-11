import { Trans } from "@lingui/macro"
import React from "react"
import { useAuthContext } from "../../../Context"

interface IThreadCTAProps {
  thread: {
    isClosed: boolean
    category: {
      isClosed: boolean
    }
  }
}

const ThreadCTA: React.FC<IThreadCTAProps> = ({ thread }) => {
  const user = useAuthContext()

  if (!user || !user.isModerator) {
    if (thread.category.isClosed) {
      return (
        <div className="thread-cta thread-cta-closed">
          <p>
            <Trans id="thread_footer.category_closed">
              This category is closed. You can't post new replies in it.
            </Trans>
          </p>
        </div>
      )
    }

    if (thread.isClosed) {
      return (
        <div className="thread-cta thread-cta-closed">
          <p>
            <Trans id="thread_footer.thread_closed">
              This thread is closed. You can't reply to it.
            </Trans>
          </p>
        </div>
      )
    }
  }

  if (!user) {
    return (
      <div className="thread-cta thread-cta-no-auth">
        <p>
          <Trans id="thread_footer.no_auth">
            Sign in to reply to this thread
          </Trans>
        </p>
      </div>
    )
  }

  return (
    <div className="thread-cta">
      <p>
        <Trans id="thread_footer.reply">
          Lorem ipsum dolor met sit amet elit.
        </Trans>
      </p>
    </div>
  )
}

export default ThreadCTA
