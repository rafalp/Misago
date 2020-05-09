import { useSelection } from "../../UI"
import { IThread } from "./Threads.types"

const useThreadsSelection = (items?: Array<IThread>) =>
  useSelection<IThread>(items)

export default useThreadsSelection
