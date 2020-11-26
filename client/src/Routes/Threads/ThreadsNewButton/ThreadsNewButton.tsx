import { Trans } from "@lingui/macro"
import classnames from "classnames"
import React from "react"
import { Link } from "react-router-dom"
import Icon from "../../../UI/Icon"
import * as urls from "../../../urls"

interface IThreadsNewButtonProps {
  category?: {
    id: string
    slug: string
  } | null
}

const ThreadsNewButton: React.FC<IThreadsNewButtonProps> = ({ category }) => (
  <Link
    className={classnames("btn btn-primary btn-responsive")}
    to={urls.postThread(category)}
  >
    <Icon icon="far fa-edit" fixedWidth />
    <span>
      <Trans id="btn.new-thread">New thread</Trans>
    </span>
  </Link>
)

export default ThreadsNewButton
