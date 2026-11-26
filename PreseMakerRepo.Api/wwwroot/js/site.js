// PreseMaker Repository — site scripts

// delay: milliseconds before it closes (default 5 s); a longer message gets longer.
function showToast(message, type, delay) {
    type = type || 'success';
    var container = document.getElementById('toastContainer');
    if (!container) return;
    var id = 'toast-' + Date.now();
    container.insertAdjacentHTML('beforeend',
        '<div id="' + id + '" class="toast align-items-center text-bg-' + type + ' border-0" role="alert">' +
        '<div class="d-flex"><div class="toast-body">' + message + '</div>' +
        '<button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>' +
        '</div></div>');
    var el = document.getElementById(id);
    new bootstrap.Toast(el, { delay: delay || 5000 }).show();
}

function escapeHtml(text) {
    var div = document.createElement('div');
    div.textContent = text == null ? '' : String(text);
    return div.innerHTML;
}

// One-click "Request Guide". The button is a link to /request-guide; with JavaScript the click records the
// request in place instead. If the call cannot be made (no token, offline, a static copy of the site) the
// link is simply followed. Requested courses are remembered in this browser for 30 days.
document.addEventListener('DOMContentLoaded', function () {
    var STORE = 'fcr.requestedGuides';
    var KEEP_MS = 30 * 24 * 3600 * 1000;
    var tokenInput = document.querySelector('#fcrAntiforgery input[name="__RequestVerificationToken"]');

    var requested = {};
    try { requested = JSON.parse(localStorage.getItem(STORE) || '{}') || {}; } catch (e) { requested = {}; }
    Object.keys(requested).forEach(function (id) {
        if (Date.now() - requested[id] > KEEP_MS) delete requested[id];
    });
    function remember(id) {
        requested[id] = Date.now();
        try { localStorage.setItem(STORE, JSON.stringify(requested)); } catch (e) { /* storage unavailable */ }
    }

    function markRequested(btn, count) {
        btn.classList.remove('btn-outline-primary', 'disabled');
        btn.classList.add('btn-success');
        btn.setAttribute('aria-disabled', 'true');
        btn.dataset.requested = '1';
        btn.textContent = 'Requested ✓';
        if (count > 0) {
            var badge = document.createElement('span');
            badge.className = 'badge text-bg-light ms-1';
            badge.textContent = count;
            btn.appendChild(badge);
        }
        btn.title = 'Guides are written in order of demand and the site is updated weekly — check back.';
    }

    function buttonsFor(id) {
        return document.querySelectorAll('.js-request-guide[data-course="' + id + '"]');
    }

    document.querySelectorAll('.js-request-guide').forEach(function (btn) {
        if (requested[btn.dataset.course]) markRequested(btn, 0);
    });

    document.addEventListener('click', function (e) {
        var btn = e.target.closest('.js-request-guide');
        if (!btn) return;
        if (btn.dataset.requested) {
            e.preventDefault();
            showToast('You have requested this guide — it is in the queue. The site is updated weekly.');
            return;
        }
        if (!tokenInput || !window.fetch || !window.FormData) return;   // follow the link
        e.preventDefault();
        if (btn.dataset.busy) return;
        btn.dataset.busy = '1';
        btn.classList.add('disabled');

        var id = btn.dataset.course;
        var body = new FormData();
        body.append('course', id);
        body.append('__RequestVerificationToken', tokenInput.value);

        fetch('/request-guide?handler=Quick', {
            method: 'POST', body: body, credentials: 'same-origin', headers: { 'Accept': 'application/json' }
        })
            .then(function (resp) {
                if (!resp.ok) throw new Error('HTTP ' + resp.status);
                return resp.json();
            })
            .then(function (data) {
                delete btn.dataset.busy;
                if (data.outcome === 'created' || data.outcome === 'alreadyRequested') {
                    remember(id);
                    buttonsFor(id).forEach(function (b) { markRequested(b, data.requestCount); });
                    // A course offered at one school (plan 15.1): the note on its own line, and time to read it.
                    var note = data.note ? '<div class="mt-2">' + escapeHtml(data.note) + '</div>' : '';
                    showToast(escapeHtml(data.message) + ' <a class="link-light" href="/queue/guides">See the queue</a>' + note,
                        'success', data.note ? 15000 : 5000);
                } else if (data.redirect) {
                    window.location.href = data.redirect;
                } else {
                    btn.classList.remove('disabled');
                    showToast(escapeHtml(data.message), 'danger');
                }
            })
            .catch(function () { window.location.href = btn.href; });
    });
});

// Course resources: the thumbs-up records (or takes back) a vote in place. Without JavaScript the form
// posts normally and the page reloads.
document.addEventListener('submit', function (e) {
    var form = e.target.closest('.js-vote-form');
    if (!form || !window.fetch || !window.FormData) return;
    e.preventDefault();
    var btn = form.querySelector('.js-vote');
    if (!btn || btn.dataset.busy) return;
    btn.dataset.busy = '1';

    fetch(form.action, {
        method: 'POST', body: new FormData(form), credentials: 'same-origin', headers: { 'Accept': 'application/json' }
    })
        .then(function (resp) {
            if (!resp.ok) throw new Error('HTTP ' + resp.status);
            return resp.json();
        })
        .then(function (data) {
            delete btn.dataset.busy;
            if (data.outcome === 'rateLimited') {
                showToast('Too many votes from your connection this hour. Please try again later.', 'danger');
                return;
            }
            var count = btn.querySelector('.vote-count');
            if (count) count.textContent = data.helpfulCount;
            btn.setAttribute('aria-pressed', data.voted ? 'true' : 'false');
            btn.classList.toggle('btn-success', !!data.voted);
            btn.classList.toggle('btn-outline-secondary', !data.voted);
            btn.title = data.voted ? 'You found this helpful — press again to take it back' : 'Found this helpful?';
        })
        .catch(function () {
            delete btn.dataset.busy;
            form.submit();          // falls back to the ordinary post
        });
});

// Course resources: a YouTube thumbnail becomes a privacy-enhanced (youtube-nocookie) player only when
// clicked, so no player loads until the visitor asks for it.
document.addEventListener('click', function (e) {
    var play = e.target.closest('.yt-lite-play');
    if (!play) return;
    var box = play.closest('.yt-lite');
    var id = box && box.dataset.video;
    if (!id || !/^[A-Za-z0-9_-]{11}$/.test(id)) return;
    var frame = document.createElement('iframe');
    frame.src = 'https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0';
    frame.title = box.dataset.title || 'YouTube video';
    frame.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
    frame.allowFullscreen = true;
    frame.referrerPolicy = 'strict-origin-when-cross-origin';
    box.replaceChildren(frame);
    frame.focus();
});

// Report modal submit
document.addEventListener('DOMContentLoaded', function () {
    var submitBtn = document.getElementById('reportSubmitBtn');
    if (!submitBtn) return;

    submitBtn.addEventListener('click', async function () {
        var endpoint = document.getElementById('reportForm').dataset.endpoint;
        var reason = document.getElementById('reportReason').value.trim();

        submitBtn.disabled = true;
        try {
            var resp = await fetch(endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ reason: reason || null })
            });
            var modal = bootstrap.Modal.getInstance(document.getElementById('reportModal'));
            if (modal) modal.hide();
            if (resp.ok) {
                showToast('Thank you — this content has been flagged for review.');
            } else {
                showToast('Could not submit report. Please try again.', 'danger');
            }
        } catch (e) {
            showToast('Could not submit report. Please try again.', 'danger');
        } finally {
            submitBtn.disabled = false;
            document.getElementById('reportReason').value = '';
        }
    });

    // Reset reason when modal closes
    var reportModal = document.getElementById('reportModal');
    if (reportModal) {
        reportModal.addEventListener('hidden.bs.modal', function () {
            document.getElementById('reportReason').value = '';
        });
    }
});

// Material inline preview toggle
document.addEventListener('DOMContentLoaded', function () {
    var previewBtn = document.getElementById('previewToggleBtn');
    var previewDiv = document.getElementById('materialPreview');
    if (!previewBtn || !previewDiv) return;

    previewBtn.addEventListener('click', function () {
        if (previewDiv.classList.contains('d-none')) {
            previewDiv.classList.remove('d-none');
            previewBtn.textContent = 'Hide Preview';
        } else {
            previewDiv.classList.add('d-none');
            previewBtn.textContent = 'Show Preview';
        }
    });
});

// The visitor counter (plan 9.3, 16.1). A page is reported once the reader does something on it: moves the
// mouse, scrolls, clicks, taps or types. Being open for a while is not enough: from 21 to 24 November 2026 a
// program running a full browser opened about 58,000 course-resources pages, waited 5 seconds on each and
// was counted as 15,000 visitors a day. Programs that never run this script or never touch the page are not
// counted, nor are browsers that say they are automated, nor events made by a script (isTrusted).
// Only the page's address and the page that linked to it are sent; the server keeps a scrambled code for the
// visitor, never the address. The layout marks which pages count (data-visit).
(function () {
    var body = document.body;
    if (!body || body.getAttribute('data-visit') !== '1' || navigator.webdriver) return;
    var sent = false;
    var events = ['pointermove', 'pointerdown', 'wheel', 'scroll', 'keydown', 'touchstart'];

    function stop() {
        events.forEach(function (e) { window.removeEventListener(e, onEvent, true); });
    }
    function onEvent(e) {
        if (e && e.isTrusted === false) return;
        if (document.visibilityState && document.visibilityState !== 'visible') return;
        send();
    }
    function send() {
        if (sent) return;
        sent = true;
        stop();
        var data = JSON.stringify({ p: location.pathname, r: document.referrer || '' });
        try {
            if (navigator.sendBeacon && navigator.sendBeacon('/visit', new Blob([data], { type: 'application/json' }))) return;
            fetch('/visit', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: data, keepalive: true })
                .catch(function () { /* counting must never disturb the page */ });
        } catch (e) { /* likewise */ }
    }
    events.forEach(function (e) { window.addEventListener(e, onEvent, { capture: true, passive: true }); });
})();

// The program panel (plan Phases 10 and 14), on the first page a browser opens in a session. The server has already set
// the session cookie that leaves it out of every later page, so the × only removes it from this one (without JavaScript
// the × is a link that reloads the page, which the cookie keeps free of it). A click on one of its links is counted
// (plan 10.4): the program and which link, sent as a beacon so the link still opens at once. Administrators are not
// counted (the layout's data-visit).
(function () {
    var panel = document.querySelector('.program-panel');
    if (!panel) return;

    var close = panel.querySelector('.js-program-close');
    if (close) close.addEventListener('click', function (e) {
        e.preventDefault();
        // Keep focus on the page by moving it to the start of the page's content (a screen reader then reads on from
        // there). Not after a tap, which could open a phone's on-screen keyboard or jump the page.
        var main = document.getElementById('main');
        var target = e.pointerType === 'touch' ? null : main;
        panel.remove();
        if (target) target.focus({ preventScroll: true });
    });
    // The × is a link acting as a button, so Space closes it too, as it would a button.
    if (close) close.addEventListener('keydown', function (e) {
        if (e.key === ' ') { e.preventDefault(); close.click(); }
    });

    if (document.body.getAttribute('data-visit') !== '1' || navigator.webdriver) return;
    function report(e) {
        if (e.type === 'auxclick' && e.button !== 1) return;   // middle-click opens a new tab; other buttons do not
        var link = e.target.closest('.js-program-link');
        if (!link) return;
        var data = JSON.stringify({ id: panel.getAttribute('data-program'), l: link.getAttribute('data-link') });
        try {
            if (navigator.sendBeacon && navigator.sendBeacon('/visit/program', new Blob([data], { type: 'application/json' }))) return;
            fetch('/visit/program', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: data, keepalive: true })
                .catch(function () { /* counting must never disturb the page */ });
        } catch (err) { /* likewise */ }
    }
    panel.addEventListener('click', report);
    panel.addEventListener('auxclick', report);
})();
