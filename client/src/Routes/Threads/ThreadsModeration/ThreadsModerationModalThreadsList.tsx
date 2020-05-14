import { Plural, Trans } from "@lingui/macro"
import React from "react"
import { ButtonSecondary, Field, TidbitReplies, Tidbits } from "../../../UI"

interface IThreadsModerationModalThreadsListProps {
  threads: Array<{
    id: string
    title: string
    replies: number
  }>
}

const ThreadsModerationModalThreadsList: React.FC<IThreadsModerationModalThreadsListProps> = ({
  threads,
}) => {
  const [isOpen, setState] = React.useState<boolean>(false)

  return (
    <Field
      label={<Trans id="moderation.selected_threads">Selected threads</Trans>}
      input={
        isOpen ? (
          <ul className="list-group selected-threads-list">
            {threads.map((thread) => (
              <li className="list-group-item" key={thread.id}>
                <div className="threads-list-thread-title">{thread.title}</div>
                <Tidbits small>
                  <TidbitReplies value={thread.replies} />
                </Tidbits>
              </li>
            ))}
          </ul>
        ) : (
          <ButtonSecondary
            text={
              <Plural
                id="moderation.see_selected_threads"
                value={threads.length}
                one="See # selected thread"
                other="See # selected threads"
              />
            }
            block
            onClick={() => setState(true)}
          />
        )
      }
    />
  )
}

export default ThreadsModerationModalThreadsList
