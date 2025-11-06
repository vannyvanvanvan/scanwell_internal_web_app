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



  function currentQueryParams() {
    // Reuse current URL query to preserve filters across SSE refreshes
    return window.location.search || "";
  }

  function buildUrlWithParams(baseUrl, extraParams) {
    var params = new URLSearchParams(window.location.search);
    if (extraParams) {
      Object.keys(extraParams).forEach(function (k) {
        if (extraParams[k] !== undefined && extraParams[k] !== null && extraParams[k] !== "") {
          params.set(k, extraParams[k]);
        }
      });
    }
    var qs = params.toString();
    return qs ? (baseUrl + "?" + qs) : baseUrl;
  }

  function onEvent(message) {
    try {
      var data = JSON.parse(message.data);
      var type = data.type;

      var hasSchedule = !!document.querySelector("#results");
      var hasSpaces = !!document.querySelector("#results-spaces");
      var hasReserve = !!document.querySelector("#results-reserve");
      var hasBooking = !!document.querySelector("#results-booking");


      if (document.visibilityState !== "visible") return; 

      // Admin/CS schedule table shows nested spaces/reserves/bookings, so refresh on all related changes
      if (hasSchedule && (type === "schedule_changed" || type === "space_changed" || type === "reserve_changed" || type === "booking_changed")) {
        // If search box has value, re-run search with filters; otherwise refresh table preserving filters
        var qInput = document.querySelector('input[name="q"]');
        var qVal = qInput && qInput.value ? qInput.value.trim() : "";
        if (qVal) {
          var searchUrl = buildUrlWithParams("/search/all", { q: qVal });
          fetchAndSwap(searchUrl, "#results");
        } else {
          var refreshUrl = buildUrlWithParams("/refresh/schedule");
          fetchAndSwap(refreshUrl, "#results");
        }
      }

      if (hasSpaces && (type === "space_changed" || type === "schedule_changed")) {
        var spaceUrl = buildUrlWithParams("/refresh/space");
        fetchAndSwap(spaceUrl, "#results-spaces");
      }

      if (hasReserve && (type === "reserve_changed" || type === "space_changed" || type === "booking_changed")) {
        var qReserve = document.querySelector('#results-reserve') ? (document.querySelector('input[name="q"]')?.value || "").trim() : "";
        if (qReserve) {
          var rUrl = buildUrlWithParams("/search/sales_reserve", { q: qReserve });
          fetchAndSwap(rUrl, "#results-reserve");
        } else {
          var rrUrl = buildUrlWithParams("/refresh/reserve");
          fetchAndSwap(rrUrl, "#results-reserve");
        }
      }

      if (hasBooking && (type === "booking_changed" || type === "space_changed")) {
        var qBooking = document.querySelector('#results-booking') ? (document.querySelector('input[name="q"]')?.value || "").trim() : "";
        if (qBooking) {
          var bUrl = buildUrlWithParams("/search/sales_booking", { q: qBooking });
          fetchAndSwap(bUrl, "#results-booking");
        } else {
          var rbUrl = buildUrlWithParams("/refresh/booking");
          fetchAndSwap(rbUrl, "#results-booking");
        }
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


