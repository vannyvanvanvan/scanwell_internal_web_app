(function () {
  function replaceInnerHTML(selector, html) {
    var el = document.querySelector(selector);
    if (el) {
      el.innerHTML = html;
    }
  }

  function fetchAndSwap(url, targetSelector) {
    var target = document.querySelector(targetSelector);
    if (!target) return;
    // Do not replace DOM while user is editing a form control inside this section
    var active = document.activeElement;
    var isFormControl = active && (/^(INPUT|SELECT|TEXTAREA)$/).test(active.tagName);
    if (isFormControl && target.contains(active)) return;

    // Capture currently expanded collapse panels within the target
    var openIds = Array.prototype.map.call(
      target.querySelectorAll('.collapse.show'),
      function (el) { return el.id; }
    );
    // Capture scroll position to avoid jumpiness
    var prevScrollTop = document.scrollingElement ? document.scrollingElement.scrollTop : window.pageYOffset;

    fetch(url, { credentials: "same-origin" })
      .then(function (res) { return res.text(); })
      .then(function (html) {
        replaceInnerHTML(targetSelector, html);
        // Restore collapse open states after swap
        openIds.forEach(function (id) {
          if (!id) return;
          var el = document.getElementById(id);
          if (el) {
            el.classList.add('show');
            // Sync the triggering button's aria-expanded if present
            var btn = document.querySelector('[data-bs-target="#' + id + '"]');
            if (btn) btn.setAttribute('aria-expanded', 'true');
          }
        });
        // Restore scroll position
        if (document.scrollingElement) {
          document.scrollingElement.scrollTop = prevScrollTop;
        } else {
          window.scrollTo(0, prevScrollTop);
        }
      })
      .catch(function () { /*
         */ });
  }

  var lastRefreshAt = {
    schedule: 0,
    reserve: 0,
    booking: 0,
  };
  var REFRESH_COOLDOWN_MS = 2000;

  function shouldRefresh(kind) {
    var now = Date.now();
    if (now - lastRefreshAt[kind] < REFRESH_COOLDOWN_MS) return false;
    lastRefreshAt[kind] = now;
    return true;
  }

  function onEvent(message) {
    try {
      var data = JSON.parse(message.data);
      var type = data.type;

      var hasSchedule = !!document.querySelector("#results");
      var hasReserve = !!document.querySelector("#results-reserve");
      var hasBooking = !!document.querySelector("#results-booking");

      if (document.visibilityState !== "visible") return; 

      // Admin/CS schedule table shows nested spaces/reserves/bookings, so refresh on all related changes
      if (hasSchedule && (type === "schedule_changed" || type === "space_changed" || type === "reserve_changed" || type === "booking_changed")) {
        // Always refresh schedule immediately to reflect nested changes
        fetchAndSwap("/refresh/schedule", "#results");
      }

      if (hasReserve && (type === "reserve_changed" || type === "space_changed")) {
        // immediate refresh for reserves
        fetchAndSwap("/refresh/reserve", "#results-reserve");
      }

      if (hasBooking && (type === "booking_changed" || type === "space_changed")) {
        fetchAndSwap("/refresh/booking", "#results-booking");
      }
    } catch (_) {
    }
  }

  try {
    var es = new EventSource("/sse/events");
    es.onmessage = onEvent;
  } catch (_) {
  }
})();


