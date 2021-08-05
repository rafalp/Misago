import { AvatarData, Settings, AuthUser } from "../../types"

const defaultSettings = {
  bulkActionLimit: 30,
  enableSiteWizard: false,
  forumIndexHeader: "",
  forumIndexThreads: true,
  forumIndexTitle: "",
  forumName: "Misago",
  passwordMinLength: 1,
  passwordMaxLength: 200,
  postMinLength: 3,
  threadTitleMinLength: 5,
  threadTitleMaxLength: 40,
  usernameMinLength: 1,
  usernameMaxLength: 10,
}

export const settingsFactory = (overrides = {}): Settings => {
  return Object.assign({}, defaultSettings, overrides)
}

const avatarSizes: Array<number> = [400, 200, 150, 100, 64, 50, 30]

export const avatarFactory = (): Array<AvatarData> => {
  let avatars: Array<AvatarData> = []
  avatarSizes.forEach((size) => {
    avatars.push({
      size,
      url: `https://placekitten.com/g/${size}/${size}`,
    })
  })
  return avatars
}

const defaultUser = {
  id: "1",
  name: "John",
  slug: "john",
  email: "john@example.com",
  isModerator: false,
  isAdmin: false,
  joinedAt: "2010-01-14T18:09:58.387Z",
  avatars: [],
  extra: {},
}

export const userFactory = (overrides = {}): AuthUser => {
  return Object.assign(
    {},
    defaultUser,
    { avatars: avatarFactory() },
    overrides
  )
}
