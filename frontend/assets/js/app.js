document.addEventListener('DOMContentLoaded', () => {
    // --- Constantes e Variáveis de Estado ---
    const API_BASE_URL_AUTH = 'http://localhost:8000/api';
    const API_BASE_URL_CONNECTIONS = 'http://localhost:8001';

    const authView = document.getElementById('auth-view');
    const mainView = document.getElementById('main-view');
    const loginForm = document.getElementById('login-form');
    const usersListDiv = document.getElementById('users-list');
    const logoutButton = document.getElementById('logout-button');
    const currentUsernameSpan = document.getElementById('current-username');

    let currentUser = null; // Armazenará os dados do usuário logado

    // --- Lógica Principal ---

    const fetchAndSetCurrentUser = async () => {
        const token = localStorage.getItem('accessToken');
        if (!token) return;

        try {
            const response = await fetch(`${API_BASE_URL_AUTH}/users/me/`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (!response.ok) {
                // Se o token for inválido, desloga o usuário
                handleLogout();
                throw new Error('Sessão inválida.');
            }
            currentUser = await response.json();
            currentUsernameSpan.textContent = currentUser.username;
        } catch (error) {
            console.error("Erro ao buscar dados do usuário:", error);
        }
    };

    const checkLoginStatus = async () => {
        const token = localStorage.getItem('accessToken');
        if (token) {
            await fetchAndSetCurrentUser();
            if (currentUser) {
                showMainView();
            }
        } else {
            showAuthView();
        }
    };

    const handleLogin = async (event) => {
        event.preventDefault();
        const formData = new FormData(loginForm);
        const data = Object.fromEntries(formData.entries());

        try {
            const response = await fetch(`${API_BASE_URL_AUTH}/token/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data),
            });
            if (!response.ok) throw new Error('Falha no login. Verifique suas credenciais.');
            const tokens = await response.json();
            localStorage.setItem('accessToken', tokens.access);
            localStorage.setItem('refreshToken', tokens.refresh);
            await checkLoginStatus();
        } catch (error) {
            console.error('Erro de login:', error);
            alert(error.message);
        }
    };

    const handleFollow = async (followedId) => {
        if (!currentUser) {
            alert("Erro: Usuário não identificado.");
            return;
        }
        const followerId = currentUser.id;

        try {
            const response = await fetch(`${API_BASE_URL_CONNECTIONS}/follow/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ follower_id: followerId, followed_id: parseInt(followedId) }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Não foi possível seguir o usuário.');
            }

            alert(`Você agora está seguindo o usuário ${followedId}!`);
            document.querySelector(`button[data-user-id='${followedId}']`).textContent = 'Seguindo';
            document.querySelector(`button[data-user-id='${followedId}']`).disabled = true;

        } catch (error) {
            console.error('Erro ao seguir:', error);
            alert(error.message);
        }
    };

    const fetchAndRenderUsers = async () => {
        try {
            const token = localStorage.getItem('accessToken');
            const response = await fetch(`${API_BASE_URL_AUTH}/users/`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (!response.ok) throw new Error('Não foi possível buscar usuários.');

            const users = await response.json();
            usersListDiv.innerHTML = ''; 

            users.forEach(user => {
                const userCard = `
                    <div class="p-4 bg-white rounded-lg shadow dark:bg-gray-800">
                        <h3 class="font-bold text-lg text-gray-800 dark:text-white">${user.username}</h3>
                        <p class="text-sm text-gray-600 dark:text-gray-400">${user.email}</p>
                        <button data-user-id="${user.id}" class="follow-btn mt-4 text-white bg-green-600 hover:bg-green-700 font-medium rounded-lg text-sm px-4 py-2">Seguir</button>
                    </div>
                `;
                usersListDiv.innerHTML += userCard;
            });

            document.querySelectorAll('.follow-btn').forEach(button => {
                button.addEventListener('click', () => handleFollow(button.dataset.userId));
            });
        } catch (error) {
            console.error('Erro ao buscar usuários:', error);
        }
    };

    const showAuthView = () => {
        authView.classList.remove('hidden');
        mainView.classList.add('hidden');
        currentUser = null;
    };

    const showMainView = () => {
        authView.classList.add('hidden');
        mainView.classList.remove('hidden');
        fetchAndRenderUsers();
    };

    const handleLogout = () => {
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        checkLoginStatus();
    };

    loginForm.addEventListener('submit', handleLogin);
    logoutButton.addEventListener('click', handleLogout);
    checkLoginStatus();
});