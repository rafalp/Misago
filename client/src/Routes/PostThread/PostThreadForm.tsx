import { Trans } from "@lingui/macro"
import React from "react"
import { Card, CardBody, CardHeader } from "../../UI/Card"
import { ICategoryChoice } from "./PostThread.types"

interface IPostThreadFormProps {
  categories: Array<ICategoryChoice>
}

const PostThreadForm: React.FC<IPostThreadFormProps> = ({ categories }) => {
  return (
    <Card>
      <CardHeader title={<Trans id="post_thread.title">New thread</Trans>} />
      <CardBody>CATEGORY, TITLE, THREAD</CardBody>
    </Card>
  )
}

export default PostThreadForm
