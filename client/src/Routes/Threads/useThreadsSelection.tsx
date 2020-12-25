import useSelection from "../../UI/useSelection"
import { Thread } from "./Threads.types"

const useThreadsSelection = (items?: Array<Thread>) =>
  useSelection<Thread>(items)

export default useThreadsSelection
