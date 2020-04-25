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

interface IHeaderProps {
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

const Header: React.FC<IHeaderProps> = ({ banner, color, text, stats }) => (
  <Card>
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

export default Header
