import React from 'react';
import { Link } from 'react-router-dom';
import './LogIn.css';

function Body() {
    return (
        <div class="log-in-body">
            <div className="join-form">
                <form>
                    <div class="input-group">
                        <label>Email:</label>
                        <input type="email" />
                    </div>
                    <div class="input-group">
                        <label>Password:</label>
                        <input type="password" />
                    </div>
                    <div class="password-reset">
                        <Link to='/Pwordreset' class="pwordreset">Password Reset</Link>
                    </div>
                    <div class="input-group">
                        <button type="submit" class="button">Log In</button>
                    </div>
                </form>
            </div>
            <div class="join-now-message">
                <span class="join-now">Not already a registered user? </span>
                <Link to='/SignUpProper' className="signup-link">Sign Up</Link>
                <span class="join-now"> with us today!</span>
            </div>
        </div>);
}

export default Body;