import { useSelection } from "../../UI"
import { IPost } from "./Thread.types"

const usePostsSelection = (items?: Array<IPost>) =>
  useSelection<IPost>(items)

export default usePostsSelection
