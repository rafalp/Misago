import React from "react"
import {
  Card,
  CardBanner,
  CardBody,
  CardColorBand,
  GridPageHeader,
} from "../../../UI"
import { IThread } from "../Thread.types"
import ThreadHeaderStarterAvatar from "./ThreadHeaderStarterAvatar"
import ThreadHeaderTidbits from "./ThreadHeaderTidbits"

interface IThreadHeaderProps {
  thread: IThread
}

const ThreadHeader: React.FC<IThreadHeaderProps> = ({ thread }) => (
  <Card className="thread-header">
    {thread.category.color && <CardColorBand color={thread.category.color} />}
    {thread.category.banner && (
      <CardBanner {...thread.category.banner.full} desktop />
    )}
    {thread.category.banner && (
      <CardBanner {...thread.category.banner.half} mobile />
    )}
    <CardBody className="thread-header-body">
      <ThreadHeaderStarterAvatar starter={thread.starter} />
      <div className="thread-header-content">
        <GridPageHeader title={thread.title} />
        <ThreadHeaderTidbits thread={thread} />
      </div>
    </CardBody>
  </Card>
)

export default React.memo(ThreadHeader)
