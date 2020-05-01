import React from "react"
import {
  Card,
  CardBanner,
  CardBody,
  CardColorBand,
  GridPageHeader,
  TidbitMembers,
  TidbitPosts,
  TidbitThreads,
  Tidbits,
} from "../../../UI"
import { ICategoryBanner } from "../../../types"

interface IThreadsHeaderProps {
  banner?: {
    full: ICategoryBanner
    half: ICategoryBanner
  } | null
  color?: string | null
  text: React.ReactNode
  stats?: {
    posts: number
    threads: number
    users?: number
  }
}

const ThreadsHeader: React.FC<IThreadsHeaderProps> = ({
  banner,
  color,
  text,
  stats,
}) => (
  <Card className="card-threads-header">
    {color && <CardColorBand color={color} />}
    {banner && <CardBanner {...banner.full} desktop />}
    {banner && <CardBanner {...banner.half} mobile />}
    <CardBody>
      <GridPageHeader
        title={text}
        sideTidbits={
          stats && (
            <Tidbits>
              <TidbitThreads value={stats.threads} />
              <TidbitPosts value={stats.posts} />
              {typeof stats.users !== "undefined" && (
                <TidbitMembers value={stats.users} />
              )}
            </Tidbits>
          )
        }
      />
    </CardBody>
  </Card>
)

export default ThreadsHeader
