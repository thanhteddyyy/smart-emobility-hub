(() => {
  const byId = id => document.getElementById(id);
  const hubs = JSON.parse(byId('hubData').textContent);
  const user = JSON.parse(byId('userData').textContent);
  const dialog = byId('booking');
  const picker = byId('stations');
  const cards = [...document.querySelectorAll('.station')];
  let hub, mode, state, alternate, map, lastBookingId = null, busy = false;
  function translate() { window.EHubI18n.applyLanguage(document.documentElement.lang || 'vi'); }
  function label(id, key) { byId(id).dataset.i18n = key; }
  function isDesktopWeb() {
    return window.EHubStudentView ? window.EHubStudentView.isDesktopWeb() : window.innerWidth >= 900;
  }
  function initMap() {
    const box = byId('liveMap');
    if (!window.L) { box.dataset.i18n = 'tv.mapOffline'; translate(); return; }
    if (!map) {
      map = L.map(box, { zoomControl: isDesktopWeb() }).setView([hub?.lat ?? 10.879, hub?.lng ?? 106.803], 15);
      L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: '© OpenStreetMap contributors' }).addTo(map);
      hubs.forEach((h, i) => L.circleMarker([h.lat, h.lng], { radius: 10 }).addTo(map).bindTooltip(Object.assign(document.createElement('span'), { textContent: h.name })).on('click', () => {
        byId('query').value = ''; filter(); selectHub(i);
      }));
    }
    setTimeout(() => map && map.invalidateSize(), 60);
  }
  function selectHub(index) {
    picker.value = String(index);
    hub = hubs[index];
    const desktop = isDesktopWeb();
    const options = [...picker.options];
    cards.forEach((card, i) => {
      card.hidden = desktop ? !!options[i]?.hidden : i !== index;
      card.classList.toggle('is-selected', i === index);
    });
    byId('empty').hidden = !!hub;
    if (map && hub) map.panTo([hub.lat, hub.lng]);
  }
  function filter() {
    const query = byId('query').value.trim().toLocaleLowerCase();
    const options = [...picker.options];
    options.forEach((option, i) => {
      const h = hubs[i];
      option.hidden = ![h.name, ...h.matchingVehicles.flatMap(v => [v.model,v.id])].join(' ').toLocaleLowerCase().includes(query);
    });
    const index = options.findIndex(option => !option.hidden);
    picker.hidden = options.filter(option => !option.hidden).length < 2;
    selectHub(index);
  }
  function syncViewMode() {
    const box = byId('liveMap');
    if (box.hidden && !box.dataset.userHidden) {
      box.hidden = false;
      initMap();
    }
    const idx = hub ? hubs.indexOf(hub) : [...picker.options].findIndex(o => !o.hidden);
    selectHub(idx);
    if (map) setTimeout(() => map.invalidateSize(), 80);
  }
  picker.onchange = () => selectHub(Number(picker.value));
  byId('query').oninput = filter;
  byId('filters').onclick = () => byId('criteria').hidden = !byId('criteria').hidden;
  byId('mapToggle').onclick = () => {
    const box = byId('liveMap');
    box.hidden = !box.hidden;
    box.dataset.userHidden = box.hidden ? '1' : '';
    if (box.hidden) return;
    initMap();
  };
  cards.forEach((card, i) => {
    card.addEventListener('click', ev => {
      if (ev.target.closest('a, button')) return;
      selectHub(i);
    });
  });
  function choose(tab) {
    mode = tab; state = null;
    const bike = mode === 'vehicle';
    byId('feedback').hidden = true;
    byId('selection').hidden = byId('tabs').hidden = false;
    byId('bikeField').hidden = byId('batteryLine').hidden = !bike;
    byId('parkField').hidden = bike;
    byId('bikeTab').classList.toggle('chosen',bike);
    byId('parkTab').classList.toggle('chosen',!bike);
    label('bookingTitle','tv.reserve'); label('confirm','tv.confirm'); label('cancel','action.cancel');
    byId('confirm').disabled = bike && !hub.matchingVehicles.length;
    translate();
  }
  function openBooking(tab = 'vehicle') {
    const vehicles = byId('vehicles');
    vehicles.replaceChildren(...hub.matchingVehicles.map(v => new Option(v.model+' (#'+v.id+')',v.id)));
    vehicles.onchange = () => byId('battery').textContent = hub.matchingVehicles[vehicles.selectedIndex]?.batteryLevel ?? '—';
    vehicles.onchange();
    byId('place').textContent = hub.name;
    if (user) byId('identity').textContent = user.id;
    else label('identity','tv.guest');
    const slot = byId('slot');
    if (slot) {
      const now = new Date();
      now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
      slot.min = now.toISOString().slice(0, 16);
    }
    choose(tab);
    if (!dialog.open) dialog.showModal();
  }
  function feedback(code) {
    state = code;
    alternate = hubs.find(h => h !== hub && h.emptySpots > 0);
    byId('selection').hidden = true;
    byId('tabs').hidden = true;
    byId('feedback').hidden = false;
    byId('feedback').dataset.state = code;
    const panels = [...dialog.querySelectorAll('[data-feedback]')];
    for (const panel of panels) panel.hidden = panel.dataset.feedback !== code;
    byId('genericFeedback').hidden = panels.some(panel => !panel.hidden);
    byId('lostBike').textContent = byId('vehicles').selectedOptions[0]?.textContent || '';
    label('feedbackTitle','tv.'+code); label('feedbackBody','tv.'+code+'Body');
    byId('alternative').textContent = code === 'HUB_FULL' && alternate ? alternate.name+' · 🅿 '+alternate.emptySpots : '';
    label('confirm', code === 'SUCCESS' && mode === 'vehicle' ? 'tv.goPickup' : code === 'HUB_FULL' && alternate ? 'tv.switch' : code === 'VEHICLE_CONFLICT' ? 'tv.find' : code === 'HOLD_EXPIRED' ? 'tv.again' : 'tv.back');
    label('cancel','tv.back'); translate();
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
  byId('cancel').onclick = () => dialog.close();
  byId('confirm').onclick = async () => {
    if (busy) return;
    if (state) {
      if (state === 'SUCCESS' && mode === 'vehicle') {
        const nextPath = lastBookingId ? '/student/pickup?bookingId=' + encodeURIComponent(lastBookingId) : '/student/pickup';
        location.assign(nextPath);
        return;
      }
      if (state === 'HUB_FULL' && alternate) {selectHub(hubs.indexOf(alternate)); openBooking('parking');}
      else if (state === 'HOLD_EXPIRED') openBooking();
      else {dialog.close(); byId('query').focus();}
      return;
    }
    if (mode === 'parking' && !byId('slot').value) {byId('slot').required=true; byId('slot').reportValidity(); return;}
    if (!user) { location.assign('/login?next=/student/search'); return; }
    busy = true; byId('confirm').disabled = true;
    try {
      const payload = mode === 'vehicle' ? {vehicleId:byId('vehicles').value} : {hubId:hub.hubId,timeSlot:byId('slot').value};
      const response = await fetch('/api/bookings/'+mode,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
      if (response.status === 401) {location.assign('/login?next=/student/search'); return;}
      const result = await response.json().catch(() => ({}));
      if (response.ok && result.ok) { lastBookingId = result.booking?.id || null; feedback('SUCCESS'); }
      else feedback(['VEHICLE_CONFLICT','HUB_FULL','HOLD_EXPIRED'].includes(result.error) ? result.error : 'UNAVAILABLE');
    } catch {feedback('UNAVAILABLE');}
    finally {busy = false; byId('confirm').disabled = false;}
  };
  filter();
  syncViewMode();
  window.addEventListener('resize', syncViewMode);
  window.addEventListener('ehub:viewchange', syncViewMode);
  // Read-only mockup previews. Never send a booking request on page load.
  const screen = new URLSearchParams(location.search).get('ui');
  const examples = {H3:'VEHICLE_CONFLICT',H4:'HUB_FULL',H5:'HOLD_EXPIRED'};
  if (hub && ['H2',...Object.keys(examples)].includes(screen)) {
    openBooking(screen === 'H4' ? 'parking' : 'vehicle');
    if (examples[screen]) feedback(examples[screen]);
  }
})();
