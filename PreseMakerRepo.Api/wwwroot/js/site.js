// PreseMaker Repository — site scripts

function showToast(message, type) {
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
    new bootstrap.Toast(el, { delay: 5000 }).show();
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
                    showToast(escapeHtml(data.message) + ' <a class="link-light" href="/queue/guides">See the queue</a>');
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
