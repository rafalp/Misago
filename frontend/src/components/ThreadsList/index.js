import React from "react"

const ThreadsList = ({ threads, isLoaded }) => {
  if (isLoaded) {
    return <div>LOADING THREADS</div>
  }

  return <div>{"Threads: " + (threads.length)}</div>
}

export default ThreadsList