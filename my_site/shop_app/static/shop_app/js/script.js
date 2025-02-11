document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('logoutButton').onclick = function () {
        window.location.href = "/accounts/logout/";
    }
});

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('loginButton').onclick = function () {
        window.location.href = "/accounts/login/";
    }
});
