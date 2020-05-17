import { Plural, Trans } from "@lingui/macro"
import React from "react"
import {
  ButtonSecondary,
  Field,
  TidbitCategory,
  TidbitReplies,
  Tidbits,
} from "../../../UI"
import { IThreadCategory } from "../Threads.types"

interface IThreadsModerationModalThreadsListProps {
  threads: Array<{
    id: string
    title: string
    replies: number
    category: IThreadCategory
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
          <ul className="list-unstyled selected-threads-list">
            {threads.map((thread) => (
              <li className="list-group-item" key={thread.id}>
                <div className="threads-list-thread-title">{thread.title}</div>
                <Tidbits small>
                  {thread.category.parent && (
                    <TidbitCategory
                      category={thread.category.parent}
                      disabled
                      parent
                    />
                  )}
                  <TidbitCategory category={thread.category} disabled />
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
