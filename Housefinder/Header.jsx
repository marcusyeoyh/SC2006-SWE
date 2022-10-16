import React from 'react';

function Header() {
    return <header>
        <a href="log-in.html" className="log-in">
            <img src="https://cdn-icons-png.flaticon.com/512/25/25694.png" alt="home icon" height="50" width="50" />
        </a>
        <h1 className="welcome-back-message">Welcome Back!</h1>
    </header>;
}

export default Header;