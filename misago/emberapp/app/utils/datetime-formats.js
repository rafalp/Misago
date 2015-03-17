import MisagoPreloadStore from 'misago/utils/preloadstore';

export function local(datetime) {
  return datetime.utcOffset(MisagoPreloadStore.get('utcOffset') / 60);
}

export default function datetimeFormats() {
  return true;
}
