import { IAvatar, ISettings, IUser } from "../../types"

const defaultSettings = {
  forumIndexHeader: "",
  forumIndexThreads: true,
  forumIndexTitle: "",
  forumName: "Misago",
  passwordMinLength: 1,
  passwordMaxLength: 40,
  usernameMinLength: 1,
  usernameMaxLength: 10,
}

export const settingsFactory = (overrides = {}): ISettings => {
  return Object.assign({}, defaultSettings, overrides)
}

const avatarSizes: Array<number> = [400, 200, 150, 100, 64, 50, 30]

export const avatarFactory = (): Array<IAvatar> => {
  let avatars: Array<IAvatar> = []
  avatarSizes.forEach(size => {
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
  isAdministrator: false,
  joinedAt: "2010-01-14T18:09:58.387Z",
  avatars: [],
  extra: {},
}

export const userFactory = (overrides = {}): IUser => {
  return Object.assign(
    {},
    defaultUser,
    { avatars: avatarFactory() },
    overrides
  )
}
