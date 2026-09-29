(function () {
    function escapeHtml(value) {
        return String(value ?? '')
            .replaceAll('&', '&amp;')
            .replaceAll('<', '&lt;')
            .replaceAll('>', '&gt;')
            .replaceAll('"', '&quot;')
            .replaceAll("'", '&#039;');
    }

    async function getSession() {
        try {
            const response = await fetch('/api/check-auth', { credentials: 'same-origin' });
            return await response.json();
        } catch (error) {
            return { authenticated: false, error: String(error) };
        }
    }

    async function logout() {
        await fetch('/api/logout', {
            method: 'POST',
            credentials: 'same-origin',
            headers: { 'Content-Type': 'application/json' },
        });
        window.location.href = '/';
    }

    async function updateNavbar() {
        const navContainer = document.querySelector('.nav-actions') || document.querySelector('.nav-buttons');
        if (!navContainer) return;

        const state = await getSession();
        if (!state.authenticated || !state.user) return;

        const user = state.user;
        const roleLabel = user.role === 'STAFF' ? 'Staff' : 'Diner';
        navContainer.innerHTML = `
            <span style="color: var(--text-muted); margin-right: 12px; font-weight: 600;">
                ${escapeHtml(user.full_name)} · ${roleLabel}
            </span>
            <a href="/reservations" class="btn-text" style="margin-right: 8px;">${user.role === 'STAFF' ? 'Staff Dashboard' : 'My Reservations'}</a>
            <button type="button" id="global-logout-btn" class="btn-primary" style="cursor:pointer; border:none;">Log Out</button>
        `;
        document.getElementById('global-logout-btn')?.addEventListener('click', logout);
    }

    window.GlobalBitesSession = { getSession, logout, updateNavbar, escapeHtml };
    document.addEventListener('DOMContentLoaded', updateNavbar);
})();
