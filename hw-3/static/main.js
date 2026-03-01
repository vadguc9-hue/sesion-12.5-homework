function showToast(message, type = "success") {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    container.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

function showAddForm() {
    document.getElementById('modal-title').textContent = 'Add New Quote';
    document.getElementById('quote-form').reset();
    document.getElementById('modal').style.display = 'flex';
    document.getElementById('quote-form').action = '/add';
}

function editQuote(id) {
    const card = document.getElementById('card-' + id);
    const text = card.querySelector('.quote-text').textContent.replace(/"/g, '');
    const author = card.querySelector('.quote-author').textContent.replace('— ', '');
    const category = card.querySelector('.quote-category').textContent;

    document.getElementById('modal-title').textContent = 'Edit Quote';
    document.getElementById('text').value = text;
    document.getElementById('author').value = author;
    document.getElementById('category').value = category;
    document.getElementById('modal').style.display = 'flex';
    document.getElementById('quote-form').action = `/edit/${id}`;
}

function closeModal() {
    document.getElementById('modal').style.display = 'none';
}

async function deleteQuote(id, button) {
    if (!confirm('Delete this quote forever?')) return;

    button.disabled = true;
    button.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';

    const res = await fetch(`/delete/${id}`, { method: 'POST' });
    const data = await res.json();

    if (data.success) {
        const card = document.getElementById('card-' + id);
        card.style.transition = 'all 0.4s';
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        setTimeout(() => card.remove(), 400);
        showToast("Quote deleted", "success");
    } else {
        showToast("Failed to delete", "error");
    }
}

// Close modal when clicking outside
document.getElementById('modal').addEventListener('click', e => {
    if (e.target.id === 'modal') closeModal();
});