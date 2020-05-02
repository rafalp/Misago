import { Trans } from "@lingui/macro"
import classNames from "classnames"
import React from "react"
import { Link } from "react-router-dom"
import { Icon } from "../../../UI"
import * as urls from "../../../urls"

interface IThreadsStartButtonProps {
  category?: {
    id: string
    slug: string
  } | null
  small?: boolean
}

const ThreadsStartButton: React.FC<IThreadsStartButtonProps> = ({
  category,
  small,
}) => (
  <Link
    className={classNames("btn btn-primary", { "btn-sm": small })}
    to={urls.startThread(category)}
  >
    <Icon icon="edit" fixedWidth />
    <span>
      <Trans id="btn.new-thread">New thread</Trans>
    </span>
  </Link>
)

export default ThreadsStartButton
