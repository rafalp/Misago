import React from "react"
import { AvatarData } from "../../types"
import blankAvatar from "./blank-avatar.png"

interface AvatarProps {
  alt?: string
  size?: number
  user?: {
    avatars: Array<AvatarData>
  } | null
}

interface AvatarSrc {
  src: string
  srcSet?: string
}

const Avatar: React.FC<AvatarProps> = ({ alt, size = 100, user = null }) => {
  if (!user) {
    return (
      <img
        alt={alt || ""}
        className="user-avatar"
        src={blankAvatar}
        width={size}
        height={size}
      />
    )
  }

  const src = findAvatarSrc(user.avatars, size)

  return (
    <img
      alt={alt || ""}
      className="user-avatar"
      width={size}
      height={size}
      {...src}
    />
  )
}

const findAvatarSrc = (
  avatars: Array<AvatarData>,
  size: number
): AvatarSrc => {
  let src = avatars[0].url
  let srcSet: string = src

  avatars.forEach((avatar) => {
    if (avatar.size >= size) {
      src = avatar.url
    }
    if (avatar.size >= size * 2) {
      srcSet = avatar.url + " 2x"
    }
  })

  if (srcSet) return { src, srcSet }
  return { src }
}

export default React.memo(Avatar)
