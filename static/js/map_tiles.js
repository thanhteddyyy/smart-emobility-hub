/* Bộ nạp bản đồ tin cậy 3 lớp cho E-Hub:
   1. Dual-CDN Leaflet (jsDelivr chính + unpkg dự phòng tự động).
   2. Tự động chuyển đổi nhiều máy chủ bản đồ miễn phí không cần API key (Esri Street -> Esri Topo -> OSM -> OSM DE) + retry từng tile.
   3. Lớp nền vector nội bộ khu vực ĐHQG-HCM hiển thị ngay dưới tilePane (không bao giờ xám trắng). */
(function () {
  const PROVIDER_KEY = "ehub-map-provider-v2";

  const TILE_PROVIDERS = [
    {
      name: "Esri World Street Map",
      url: "https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",
      options: {
        maxZoom: 19,
        attribution: "Tiles © Esri",
      },
    },
    {
      name: "Esri World Topo Map",
      url: "https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}",
      options: {
        maxZoom: 19,
        attribution: "Tiles © Esri",
      },
    },
    {
      name: "OpenStreetMap",
      url: "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
      options: {
        maxZoom: 19,
        attribution: "© OpenStreetMap contributors",
      },
    },
    {
      name: "OpenStreetMap DE",
      url: "https://tile.openstreetmap.de/{z}/{x}/{y}.png",
      options: {
        maxZoom: 19,
        attribution: "© OpenStreetMap contributors",
      },
    },
  ];

  const readyQueue = [];
  const errorQueue = [];
  let fallbackTried = false;
  let failedAll = false;

  function flushQueue(queue) {
    const callbacks = queue.splice(0, queue.length);
    callbacks.forEach(function (fn) {
      try {
        fn();
      } catch (err) {
        console.error("[EHubMap] callback error:", err);
      }
    });
  }

  function _notifyReady() {
    if (!window.L) return;
    errorQueue.length = 0;
    flushQueue(readyQueue);
  }

  function _loadFallbackLeaflet() {
    if (window.L) {
      _notifyReady();
      return;
    }
    if (fallbackTried) {
      failedAll = true;
      readyQueue.length = 0;
      flushQueue(errorQueue);
      return;
    }
    fallbackTried = true;
    const script = document.createElement("script");
    script.src = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js";
    script.onload = _notifyReady;
    script.onerror = function () {
      failedAll = true;
      readyQueue.length = 0;
      flushQueue(errorQueue);
    };
    document.head.appendChild(script);
  }

  function onReady(cb, onError) {
    if (window.L) {
      if (typeof cb === "function") {
        try {
          cb();
        } catch (err) {
          console.error("[EHubMap] init error:", err);
        }
      }
      return;
    }
    if (failedAll) {
      if (typeof onError === "function") onError();
      return;
    }
    if (typeof cb === "function") readyQueue.push(cb);
    if (typeof onError === "function") errorQueue.push(onError);
  }

  function readToken(name, fallback) {
    try {
      const value = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
      return value || fallback;
    } catch (e) {
      return fallback;
    }
  }

  function addCampusUnderlay(map) {
    if (!map || !window.L || map._ehubUnderlayAdded) return;
    map._ehubUnderlayAdded = true;

    const pane = map.getPane("ehubCampusUnderlay") || map.createPane("ehubCampusUnderlay");
    pane.style.zIndex = "150";
    pane.style.pointerEvents = "none";

    const gridLayers = [];
    const parkLayers = [];
    const waterLayers = [];
    const roadCasingLayers = [];
    const roadCoreLayers = [];
    const metroLayers = [];

    function getMapPalette() {
      return {
        park: readToken("--map-park", "#d6ecd9"),
        parkStroke: readToken("--map-park-stroke", "#b7dcc0"),
        water: readToken("--map-water", "#bfe0f7"),
        waterStroke: readToken("--map-water-stroke", "#8ec2eb"),
        road: readToken("--map-road", "#ffffff"),
        roadCasing: readToken("--map-road-casing", "#cbd5e1"),
        metro: readToken("--map-metro", "#49beff"),
        grid: readToken("--map-grid", "rgba(42, 53, 71, 0.08)"),
      };
    }

    const palette = getMapPalette();

    // 1. Lưới tọa độ nhẹ bao phủ KĐT ĐHQG-HCM
    for (let lat = 10.858; lat <= 10.8921; lat += 0.004) {
      gridLayers.push(
        L.polyline(
          [
            [lat, 106.772],
            [lat, 106.818],
          ],
          { pane: "ehubCampusUnderlay", interactive: false, color: palette.grid, weight: 1 }
        ).addTo(map)
      );
    }
    for (let lng = 106.772; lng <= 106.8181; lng += 0.004) {
      gridLayers.push(
        L.polyline(
          [
            [10.858, lng],
            [10.892, lng],
          ],
          { pane: "ehubCampusUnderlay", interactive: false, color: palette.grid, weight: 1 }
        ).addTo(map)
      );
    }

    // 2. Các phân khu khuôn viên xanh (BK CS2, KTX Khu A, KTX Khu B, NVH Sinh viên)
    const campusZones = [
      [[10.8792, 106.8035], [10.8826, 106.8035], [10.8826, 106.8078], [10.8792, 106.8078]],
      [[10.8764, 106.8042], [10.8790, 106.8042], [10.8790, 106.8086], [10.8764, 106.8086]],
      [[10.8808, 106.7802], [10.8848, 106.7802], [10.8848, 106.7852], [10.8808, 106.7852]],
      [[10.8736, 106.7988], [10.8768, 106.7988], [10.8768, 106.8028], [10.8736, 106.8028]],
    ];
    campusZones.forEach(function (coords) {
      parkLayers.push(
        L.polygon(coords, {
          pane: "ehubCampusUnderlay",
          interactive: false,
          color: palette.parkStroke,
          weight: 1.5,
          fillColor: palette.park,
          fillOpacity: 0.9,
        }).addTo(map)
      );
    });

    // 3. Hồ Đá
    waterLayers.push(
      L.polygon(
        [
          [10.8812, 106.7938],
          [10.8838, 106.7955],
          [10.8832, 106.7988],
          [10.8800, 106.7992],
          [10.8788, 106.7962],
        ],
        {
          pane: "ehubCampusUnderlay",
          interactive: false,
          color: palette.waterStroke,
          weight: 1.5,
          fillColor: palette.water,
          fillOpacity: 0.92,
        }
      ).addTo(map)
    );

    // 4. Các trục đường chính nối 5 Hub
    const roads = [
      {
        coords: [[10.8615, 106.7840], [10.8648, 106.7950], [10.8664, 106.8010], [10.8688, 106.8085], [10.8725, 106.8155]],
        casingWeight: 10,
        coreWeight: 6.5,
      },
      {
        coords: [[10.8664, 106.8010], [10.8710, 106.8005], [10.8752, 106.8007], [10.8783, 106.8063], [10.8806, 106.8054], [10.8845, 106.8050]],
        casingWeight: 7,
        coreWeight: 4.5,
      },
      {
        coords: [[10.8752, 106.8007], [10.8772, 106.7955], [10.8795, 106.7895], [10.8826, 106.7825], [10.8855, 106.7775]],
        casingWeight: 7,
        coreWeight: 4.5,
      },
      {
        coords: [[10.8806, 106.8054], [10.8822, 106.8005], [10.8842, 106.7935], [10.8826, 106.7825]],
        casingWeight: 6,
        coreWeight: 3.5,
      },
      {
        coords: [[10.8826, 106.7825], [10.8745, 106.7855], [10.8648, 106.7950]],
        casingWeight: 6,
        coreWeight: 3.5,
      },
    ];

    roads.forEach(function (road) {
      roadCasingLayers.push(
        L.polyline(road.coords, {
          pane: "ehubCampusUnderlay",
          interactive: false,
          color: palette.roadCasing,
          weight: road.casingWeight,
          lineCap: "round",
          lineJoin: "round",
        }).addTo(map)
      );
      roadCoreLayers.push(
        L.polyline(road.coords, {
          pane: "ehubCampusUnderlay",
          interactive: false,
          color: palette.road,
          weight: road.coreWeight,
          lineCap: "round",
          lineJoin: "round",
        }).addTo(map)
      );
    });

    // Tuyến Metro số 1 chạy song song phía bắc Xa lộ Hà Nội
    metroLayers.push(
      L.polyline(
        [
          [10.8619, 106.7840],
          [10.8652, 106.7950],
          [10.8668, 106.8010],
          [10.8692, 106.8085],
          [10.8729, 106.8155],
        ],
        {
          pane: "ehubCampusUnderlay",
          interactive: false,
          color: palette.metro,
          weight: 3,
          dashArray: "8 6",
        }
      ).addTo(map)
    );

    // 5. Nhãn khu vực nội bộ
    [
      { pos: [10.8814, 106.7966], text: "Hồ Đá" },
      { pos: [10.8768, 106.7960], text: "KĐT ĐHQG-HCM" },
      { pos: [10.8654, 106.8008], text: "Xa lộ Hà Nội · Metro #1" },
    ].forEach(function (item) {
      L.marker(item.pos, {
        pane: "ehubCampusUnderlay",
        interactive: false,
        keyboard: false,
        icon: L.divIcon({
          className: "ehub-map-label",
          iconSize: null,
          html: item.text,
        }),
      }).addTo(map);
    });

    // Đồng bộ màu nền vector khi đổi Sáng/Tối
    if (typeof MutationObserver !== "undefined") {
      const themeObserver = new MutationObserver(function () {
        const next = getMapPalette();
        gridLayers.forEach(function (l) { l.setStyle({ color: next.grid }); });
        parkLayers.forEach(function (l) { l.setStyle({ color: next.parkStroke, fillColor: next.park }); });
        waterLayers.forEach(function (l) { l.setStyle({ color: next.waterStroke, fillColor: next.water }); });
        roadCasingLayers.forEach(function (l) { l.setStyle({ color: next.roadCasing }); });
        roadCoreLayers.forEach(function (l) { l.setStyle({ color: next.road }); });
        metroLayers.forEach(function (l) { l.setStyle({ color: next.metro }); });
      });
      themeObserver.observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
      map.on("unload", function () { themeObserver.disconnect(); });
    }
  }

  function attachBaseLayer(map) {
    if (!map || !window.L) return;

    addCampusUnderlay(map);

    let savedIdx = 0;
    try {
      const raw = parseInt(sessionStorage.getItem(PROVIDER_KEY), 10);
      if (!isNaN(raw) && raw >= 0 && raw < TILE_PROVIDERS.length) {
        savedIdx = raw;
      }
    } catch (e) {}

    let activeLayer = null;
    let watchdog = null;
    let recoveryTimer = null;
    let exhausted = false;
    let tileLoadedCount = 0;
    let unloaded = false;

    function tryProvider(startIdx, attemptCount) {
      if (unloaded) return;

      clearTimeout(watchdog);
      clearTimeout(recoveryTimer);

      if (attemptCount >= TILE_PROVIDERS.length) {
        if (activeLayer) {
          map.removeLayer(activeLayer);
          activeLayer = null;
        }
        exhausted = true;
        if (navigator.onLine !== false) {
          recoveryTimer = setTimeout(function () {
            if (!unloaded && exhausted) tryProvider(0, 0);
          }, 20000);
        }
        return;
      }

      exhausted = false;
      const idx = (startIdx + attemptCount) % TILE_PROVIDERS.length;
      const provider = TILE_PROVIDERS[idx];

      if (activeLayer) {
        map.removeLayer(activeLayer);
      }

      const layer = L.tileLayer(
        provider.url,
        Object.assign({}, provider.options, {
          keepBuffer: 4,
          updateWhenIdle: false,
          updateWhenZooming: false,
        })
      );
      activeLayer = layer;

      let loaded = 0;
      let errors = 0;
      let switched = false;

      function failover() {
        if (unloaded || switched || activeLayer !== layer) return;
        switched = true;
        clearTimeout(watchdog);
        tryProvider(startIdx, attemptCount + 1);
      }

      layer.on("tileload", function () {
        loaded += 1;
        tileLoadedCount = loaded;
        clearTimeout(watchdog);
        try {
          sessionStorage.setItem(PROVIDER_KEY, String(idx));
        } catch (e) {}
      });

      layer.on("tileerror", function (ev) {
        if (unloaded || switched || activeLayer !== layer) return;
        const img = ev && ev.tile;
        if (loaded > 0 && img && img.src) {
          const tries = Number(img.dataset.ehubRetry || 0);
          if (tries < 2) {
            img.dataset.ehubRetry = String(tries + 1);
            const delay = tries === 0 ? 600 : 1800;
            const cleanSrc = img.src.replace(/([?&])ehub_r=\d+/g, "").replace(/[?&]$/, "");
            setTimeout(function () {
              if (!unloaded && activeLayer === layer) {
                img.src = cleanSrc + (cleanSrc.indexOf("?") >= 0 ? "&" : "?") + "ehub_r=" + (tries + 1);
              }
            }, delay);
          } else {
            img.style.opacity = "0";
          }
          return;
        }
        errors += 1;
        if (errors >= 2) failover();
      });

      watchdog = setTimeout(function () {
        if (!unloaded && activeLayer === layer && loaded === 0) failover();
      }, 3500);

      layer.addTo(map);
    }

    tryProvider(savedIdx, 0);

    function refreshSize() {
      if (unloaded || !map || !map._container) return;
      try {
        map.invalidateSize({ animate: false });
      } catch (e) {}
    }

    function onViewChange() {
      refreshSize();
      if (typeof requestAnimationFrame === "function") requestAnimationFrame(refreshSize);
      setTimeout(refreshSize, 200);
    }

    function onOnline() {
      if (!unloaded && (exhausted || tileLoadedCount === 0)) {
        tryProvider(0, 0);
      }
    }

    let resizeObserver = null;
    if (typeof ResizeObserver !== "undefined" && map.getContainer()) {
      resizeObserver = new ResizeObserver(refreshSize);
      resizeObserver.observe(map.getContainer());
    }

    window.addEventListener("ehub:viewchange", onViewChange);
    window.addEventListener("resize", refreshSize);
    window.addEventListener("load", refreshSize);
    window.addEventListener("online", onOnline);

    map.on("unload", function () {
      unloaded = true;
      clearTimeout(watchdog);
      clearTimeout(recoveryTimer);
      if (resizeObserver) resizeObserver.disconnect();
      window.removeEventListener("ehub:viewchange", onViewChange);
      window.removeEventListener("resize", refreshSize);
      window.removeEventListener("load", refreshSize);
      window.removeEventListener("online", onOnline);
    });
  }

  window.EHubMap = {
    TILE_PROVIDERS: TILE_PROVIDERS,
    onReady: onReady,
    addCampusUnderlay: addCampusUnderlay,
    attachBaseLayer: attachBaseLayer,
    _notifyReady: _notifyReady,
    _loadFallbackLeaflet: _loadFallbackLeaflet,
  };
})();

