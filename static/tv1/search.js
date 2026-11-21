(() => {
  const byId = id => document.getElementById(id);
  const hubs = JSON.parse(byId('hubData').textContent);
  const user = JSON.parse(byId('userData').textContent);
  const dialog = byId('booking');
  const query = byId('query');
  const suggestions = byId('suggestions');
  const choices = [...suggestions.querySelectorAll('button')];
  const cards = [...document.querySelectorAll('.station')];
  const origin = JSON.parse(byId('originData').textContent);
  const slot = byId('slot');
  let hub, mode, state, alternate, map, route, lastBookingId = null, busy = false;
  function translate() { window.EHubI18n.applyLanguage(document.documentElement.lang || 'vi'); }
  function label(id, key) { byId(id).dataset.i18n = key; }

  function initMap() {
    const box = byId('liveMap');
    if (!window.L || !origin) {
      box.dataset.i18n = 'tv.mapOffline';
      translate();
      return;
    }
    const start = [origin.lat, origin.lng];
    map = L.map(box).setView(start, 15);
    map.zoomControl.setPosition('bottomleft');
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: '© OpenStreetMap contributors' }).addTo(map);
    hubs.forEach((h, i) => L.circleMarker([h.lat, h.lng], { radius: 11 })
      .addTo(map).bindTooltip(Object.assign(document.createElement('span'), { textContent: h.name }))
      .on('click', () => selectHub(i)));
    const markerLabel = document.createElement('span');
    markerLabel.dataset.i18n = 'tv.origin';
    markerLabel.textContent = 'BK CS2';
    L.circleMarker(start, { radius: 5, interactive: false, color: 'white', fillColor: 'blue', fillOpacity: 1 })
      .addTo(map).bindTooltip(markerLabel, { permanent: true, direction: 'bottom' });
    new ResizeObserver(() => map.invalidateSize()).observe(box);
  }

  function selectHub(index) {
    hub = hubs[index];
    suggestions.hidden = true;
    byId('sheet').hidden = !hub;
    query.value = hub?.name || '';
    cards.forEach((card, i) => { card.hidden = i !== index; });
    if (route) { route.remove(); route = null; }
    if (!map) return;
    map.invalidateSize();
    const start = [origin.lat, origin.lng];
    if (!hub) { map.setView(start, 15); return; }
    const end = [hub.lat, hub.lng];
    if (hub.lat === origin.lat && hub.lng === origin.lng) map.setView(start, 16);
    else {
      route = L.polyline([start, end], { dashArray: '5 8', interactive: false }).addTo(map);
      map.fitBounds(route.getBounds(), { padding: [30, 50], maxZoom: 16 });
    }
  }

  function normalize(value) {
    return value.normalize('NFD').replace(/\p{M}/gu, '').toLowerCase().replaceAll('đ', 'd');
  }
  function suggest() {
    const term = normalize(query.value.trim()).replace('ky tuc xa', 'ktx');
    choices.forEach((button, i) => { button.parentElement.hidden = !normalize(hubs[i].name).includes(term); });
    byId('noMatches').hidden = choices.some(button => !button.parentElement.hidden);
    suggestions.hidden = false;
  }
  choices.forEach((button, i) => { button.onclick = () => selectHub(i); });
  query.onfocus = suggest;
  query.onclick = suggest;
  query.oninput = () => {
    const value = query.value;
    selectHub(-1);
    query.value = value;
    suggest();
  };
  query.onkeydown = event => {
    const first = choices.find(button => !button.parentElement.hidden);
    if (event.key === 'ArrowDown' && first) { event.preventDefault(); first.focus(); }
    if (event.key === 'Enter' && first && !suggestions.hidden) first.click();
  };
  document.addEventListener('keydown', event => { if (event.key === 'Escape') suggestions.hidden = true; });
  document.addEventListener('click', event => {
    if (!suggestions.contains(event.target) && event.target !== query) suggestions.hidden = true;
  });
  byId('closeSheet').onclick = () => selectHub(-1);

  function updateMinimum() {
    const next = new Date((Math.floor(Date.now() / 60000) + 1) * 60000);
    slot.min = new Date(next.getTime() - next.getTimezoneOffset() * 60000).toISOString().slice(0, 16);
  }
  slot.onfocus = updateMinimum;
  function choose(tab) {
    mode = tab; state = null;
    const bike = mode === 'vehicle';
    byId('feedback').hidden = true;
    byId('selection').hidden = byId('tabs').hidden = false;
    byId('bikeField').hidden = byId('batteryLine').hidden = !bike;
    byId('parkField').hidden = bike;
    byId('bikeTab').classList.toggle('chosen', bike);
    byId('parkTab').classList.toggle('chosen', !bike);
    label('bookingTitle', 'tv.reserve'); label('confirm', 'tv.confirm'); label('cancel', 'action.cancel');
    byId('cancel').hidden = false;
    byId('confirm').disabled = false;
    updateMinimum();
    translate();
  }
  function openBooking(tab = 'vehicle') {
    const vehicles = byId('vehicles');
    const available = hub.matchingVehicles;
    vehicles.replaceChildren(...available.map(v => new Option(v.model + ' (#' + v.id + ')', v.id)));
    vehicles.onchange = () => byId('battery').textContent = available[vehicles.selectedIndex]?.batteryLevel ?? '—';
    vehicles.onchange();
    byId('place').textContent = hub.name;
    if (user) byId('identity').textContent = user.id;
    else label('identity', 'tv.guest');

    choose(tab);
    if (!dialog.open) dialog.showModal();
  }
  function feedback(code) {
    state = code;
    alternate = hubs.find(h => h !== hub && h.status === 'ACTIVE' && h.emptySpots > 0);
    byId('selection').hidden = true;
    byId('tabs').hidden = true;
    byId('feedback').hidden = false;
    byId('feedback').dataset.state = code;
    const panels = [...dialog.querySelectorAll('[data-feedback]')];
    for (const panel of panels) panel.hidden = panel.dataset.feedback !== code;
    byId('genericFeedback').hidden = panels.some(panel => !panel.hidden);
    byId('lostBike').textContent = byId('vehicles').selectedOptions[0]?.textContent || '';
    label('feedbackTitle', 'tv.' + code); label('feedbackBody', 'tv.' + code + 'Body');
    byId('alternative').textContent = code === 'HUB_FULL' && alternate ? alternate.name + ' · 🅿 ' + alternate.emptySpots : '';
    const actions = {
      SUCCESS: mode === 'vehicle' ? 'tv.goPickup' : 'tv.done',
      HUB_FULL: alternate ? 'tv.switch' : 'tv.back',
      VEHICLE_CONFLICT: 'tv.find',
      NO_BIKES: 'tv.find',
      HOLD_EXPIRED: 'tv.again',
      UNAVAILABLE: 'tv.again',
      INVALID_PARAMETERS: 'tv.again'
    };
    byId('cancel').hidden = actions[code] === 'tv.done' || actions[code] === 'tv.back';
    label('confirm', actions[code]);
    label('cancel', 'tv.back'); translate();
  }
  byId('bikeTab').onclick = () => choose('vehicle');
  byId('parkTab').onclick = () => choose('parking');
  document.querySelectorAll('[data-book]').forEach(button => {
    button.onclick = () => {
      const card = button.closest('.station');
      if (card) selectHub(Number(card.dataset.index));
      openBooking();
    };
  });
  byId('cancel').onclick = () => { dialog.close(); if (state) selectHub(-1); };
  byId('confirm').onclick = async () => {
    if (busy) return;
    if (state) {
      if (state === 'SUCCESS' && mode === 'vehicle') {
        const nextPath = lastBookingId ? '/student/pickup?bookingId=' + encodeURIComponent(lastBookingId) : '/student/pickup';
        location.assign(nextPath);
        return;
      }
      if (state === 'HUB_FULL' && alternate) { selectHub(hubs.indexOf(alternate)); openBooking('parking'); }
      else if (['HOLD_EXPIRED', 'UNAVAILABLE', 'INVALID_PARAMETERS'].includes(state)) openBooking(mode);
      else { dialog.close(); selectHub(-1); if (['VEHICLE_CONFLICT', 'NO_BIKES'].includes(state)) query.focus(); }
      return;
    }
    updateMinimum();
    if (mode === 'parking' && !slot.reportValidity()) return;
    if (mode === 'vehicle' && !byId('vehicles').value) { feedback('NO_BIKES'); return; }
    if (!user) { location.assign('/login?next=/student/search'); return; }
    busy = true;
    dialog.querySelectorAll('button, input, select').forEach(el => { el.disabled = true; });
    try {
      const payload = mode === 'vehicle' ? { vehicleId: byId('vehicles').value } : { hubId: hub.hubId, timeSlot: new Date(slot.value).toISOString() };
      const response = await fetch('/api/bookings/' + mode, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
      if (response.status === 401) { location.assign('/login?next=/student/search'); return; }
      const result = await response.json().catch(() => ({}));
      if (response.ok && result.ok) {
        lastBookingId = result.booking?.id || null;
        if (mode === 'vehicle') hub.matchingVehicles = hub.matchingVehicles.filter(v => v.id !== payload.vehicleId);
        const key = mode === 'vehicle' ? 'availableVehicles' : 'emptySpots';
        hub[key] = Math.max(0, hub[key] - 1);
        cards[hubs.indexOf(hub)].querySelector('[data-rt$=".' + key + '"]').textContent = hub[key];
        feedback('SUCCESS');
      }
      else feedback(['VEHICLE_CONFLICT', 'HUB_FULL', 'HOLD_EXPIRED', 'INVALID_PARAMETERS'].includes(result.error) ? result.error : 'UNAVAILABLE');
    } catch { feedback('UNAVAILABLE'); }
    finally {
      busy = false;
      dialog.querySelectorAll('button, input, select').forEach(el => { el.disabled = false; });
    }
  };
  dialog.addEventListener('cancel', event => { if (busy) event.preventDefault(); });
  const models = new Map(hubs.flatMap(h => h.matchingVehicles.map(v => [v.id, v.model])));
  document.addEventListener('ehub:state', ({ detail }) => {
    const vehicles = Object.entries(detail.network.vehicles);
    hubs.forEach((h, i) => {
      Object.assign(h, detail.hubs[h.hubId]);
      h.matchingVehicles = vehicles.filter(([, v]) => v.hubId === h.hubId && v.status === 'AVAILABLE')
        .map(([id, v]) => ({ ...v, id, model: models.get(id) || id }));
      const pill = cards[i].querySelector('.pill');
      const key = h.availableVehicles ? 'tv.open' : 'tv.noBike';
      if (pill.dataset.i18n !== key) { pill.dataset.i18n = key; translate(); }
    });
  });
  initMap();
  // Read-only mockup previews. Never send a booking request on page load.
  const screen = new URLSearchParams(location.search).get('ui');
  const examples = { H3: 'VEHICLE_CONFLICT', H4: 'HUB_FULL', H5: 'HOLD_EXPIRED' };
  if (hubs.length && ['H2', ...Object.keys(examples)].includes(screen)) {
    selectHub(0);
    openBooking(screen === 'H4' ? 'parking' : 'vehicle');
    if (examples[screen]) feedback(examples[screen]);
  }
})();
