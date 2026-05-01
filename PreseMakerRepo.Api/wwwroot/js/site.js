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
