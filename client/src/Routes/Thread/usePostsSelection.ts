import useSelection from "../../UI/useSelection"
import { IPost } from "./Thread.types"

const usePostsSelection = (items?: Array<IPost>) => useSelection<IPost>(items)

export default usePostsSelection
