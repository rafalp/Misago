export var initialState = {
  tick: 0,
}

export const TICK = "TICK"

export function doTick() {
  return {
    type: TICK,
  }
}

export default function tick(state = initialState, action = null) {
  if (action.type === TICK) {
    return Object.assign({}, state, {
      tick: state.tick + 1,
    })
  } else {
    return state
  }
}
