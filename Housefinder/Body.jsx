import React from 'react';

function Body() {
    return(
    <div class="sign-up-link">
        <form class="join-form">
            <div class="input-group">
                <label>Email:</label>
                <input type="email" />
            </div>
            <div class="input-group">
                <label>Password:</label>
                <input type="password" />
            </div>
            <div class="password-reset">
                <a href="passwordreset.html" class="pwordreset">Password Reset</a>
            </div>
            <div class="input-group">
                <button type="submit" class="button">Log In</button>
            </div>
        </form>
        <div class="join-now-message">
            <span class="join-now">Not already a registered user? </span>
            <a href="signup.html" class="signup-link">Sign Up</a>
            <span class="join-now"> with us today!</span>
        </div>
    </div>);
}

export default Body;