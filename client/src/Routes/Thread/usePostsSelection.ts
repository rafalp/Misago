import useSelection from "../../UI/useSelection"
import { Post } from "./Thread.types"

const usePostsSelection = (items?: Array<Post>) => useSelection<Post>(items)

export default usePostsSelection
